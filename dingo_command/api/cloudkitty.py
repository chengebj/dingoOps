# 计费的api接口
import os
from typing import List
from oslo_log import log

from fastapi.responses import FileResponse, StreamingResponse
from urllib.parse import unquote
from starlette.background import BackgroundTask

from dingo_command.api.model.cloudkitty import CloudKittyRatingSummaryDetail, RatingModuleConfigHashMapMapping, RatingModuleConfigHashMapThreshold, RatingModules
from dingo_command.services.cloudkitty import CloudKittyService
from dingo_command.utils import file_utils

from dingo_command.utils.constant import EXCEL_TEMP_DIR
from dingo_command.utils.datetime import format_d8q_timestamp
from fastapi import APIRouter, HTTPException, Query

LOG = log.getLogger(__name__)
router = APIRouter()

cloudkitty_service = CloudKittyService()

@router.get("/cloudkitty/download/ratingSummary/execl", summary="下载计费汇总execl表格", description="下载计费汇总execl表格")
async def download_rating_summary_execl(begin: str = Query(None, description="开始时间"),
                                        end: str = Query(None, description="结束时间时间"),
                                        tenant_id: str = Query(None, description="项目ID"),
                                        resource_type: str = Query(None, description="资源类型")):
    # 把数据库中的资产数据导出资产信息数据
    result_file_name = "rating_summary_" + format_d8q_timestamp() + ".xlsx"
    # 导出文件路径
    result_file_path = EXCEL_TEMP_DIR + result_file_name
    # 生成文件
    # 读取excel文件内容
    try:
        # 声明查询条件的dict
        query_params = {}
        if begin:
            query_params['begin'] = begin
        if end:
            query_params['end'] = end
        if tenant_id:
            query_params['tenant_id'] = tenant_id
        if resource_type:
            query_params['resource_type'] = resource_type
        # 生成文件
        cloudkitty_service.download_rating_summary_excel(result_file_path, query_params)
    except Exception as e:
        import traceback
        traceback.print_exc()
        file_utils.cleanup_temp_file(result_file_path)
        raise HTTPException(status_code=400, detail="generate execl file error")

    # 文件存在则下载
    if os.path.exists(result_file_path):
        return FileResponse(
            path=result_file_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=result_file_name,  # 下载时显示的文件名
            background = BackgroundTask(file_utils.cleanup_temp_file, result_file_path)
        )
    raise HTTPException(status_code=400, detail="Execl file not found")

@router.post("/cloudkitty/download/ratingSummaryDetail/pdf/preprocessing", summary="预处理下载计费汇总详情需要的PDF文件", description="预处理下载计费汇总详情需要的PDF文件")
async def download_rating_summary_detail_pdf_preprocessing(detail: List[CloudKittyRatingSummaryDetail],
                                             language: str = Query(None, description="当前环境语言")):
    result_file_pdf_name = "rating_summary_detail_" + format_d8q_timestamp() + ".pdf"
    # 导出文件路径
    result_file_pdf_path = EXCEL_TEMP_DIR + result_file_pdf_name

    # 1. 生成PDF文件
    try:
        cloudkitty_service.generate_rating_summary_detail_pdf(result_file_pdf_path, detail, language)
        return os.path.basename(result_file_pdf_path)
    except Exception as e:
        import traceback
        traceback.print_exc()
        file_utils.cleanup_temp_file(result_file_pdf_path)
        raise HTTPException(status_code=400, detail="generate pdf file error")

@router.get("/cloudkitty/download/ratingSummaryDetail/pdf", summary="下载计费汇总详情PDF", description="下载计费汇总详情PDF")
async def download_rating_summary_detail_pdf(filePath: str = Query(None, description="下载PDF文件名称")):
    # 文件存在则下载
    result_file_pdf_path = EXCEL_TEMP_DIR + unquote(filePath)
    LOG.info(f"rating summary detail download pdf name：{filePath}, path: {result_file_pdf_path}, isExists:{os.path.exists(result_file_pdf_path)}")
    if filePath is not None and os.path.exists(result_file_pdf_path):
        return FileResponse(
            path=result_file_pdf_path,
            media_type="application/octet-stream",
            filename=unquote(filePath),  # 下载时显示的文件名
            background=BackgroundTask(file_utils.cleanup_temp_file, result_file_pdf_path)
        )
    raise HTTPException(status_code=400, detail="PDf file not found")

@router.post("/cloudkitty/download/ratingSummaryDetail/pdf", summary="下载计费汇总详情PDF文件", description="下载计费汇总详情PDF文件")
async def rating_summary_detail_pdf_download(detail: List[CloudKittyRatingSummaryDetail],
                                             language: str = Query(None, description="当前环境语言")):
    result_file_pdf_name = "rating_summary_detail_" + format_d8q_timestamp() + ".pdf"
    # 导出文件路径
    result_file_pdf_path = EXCEL_TEMP_DIR + result_file_pdf_name

    # 1. 生成PDF文件
    try:
        cloudkitty_service.generate_rating_summary_detail_pdf(result_file_pdf_path, detail, language)
    except Exception as e:
        import traceback
        traceback.print_exc()
        file_utils.cleanup_temp_file(result_file_pdf_path)
        raise HTTPException(status_code=400, detail="generate pdf file error")

    if not os.path.exists(result_file_pdf_path):
        raise HTTPException(status_code=404, detail="PDf file not found")

    def file_stream():
        with open(result_file_pdf_path, "rb") as f:
            while chunk := f.read(8192):  # 8KB分块读取
                yield chunk
        file_utils.cleanup_temp_file(result_file_pdf_path)

    return StreamingResponse(
        file_stream(),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={result_file_pdf_name}"}
    )

# @router.post("/cloudkitty/download/ratingSummaryDetail/execl", summary="下载计费汇总详情execl", description="下载计费汇总详情execl")
# async def download_rating_summary_detail_execl(detail: List[CloudKittyRatingSummaryDetail],
#                                              language: str = Query(None, description="当前环境语言")):
#     result_file_execl_name = "rating_summary_detail_" + format_d8q_timestamp() + ".xlsx"
#     # 导出文件路径
#     result_file_execl_path = EXCEL_TEMP_DIR + result_file_execl_name
#
#     # 1. 生成Excel文件
#     try:
#         cloudkitty_service.download_rating_summary_detail_execl(result_file_execl_path, detail, language)
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         file_utils.cleanup_temp_file(result_file_execl_path)
#         raise HTTPException(status_code=400, detail="generate execl file error")
#
#     # 文件存在则下载
#     if os.path.exists(result_file_execl_path):
#         return FileResponse(
#             path=result_file_execl_path,
#             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#             filename=result_file_execl_name,  # 下载时显示的文件名
#             background=BackgroundTask(file_utils.cleanup_temp_file, result_file_execl_path)
#         )
#     raise HTTPException(status_code=400, detail="Execl file not found")

@router.put("/cloudkitty/module_config/hashmap/mappings/{mapping_id}", summary="编辑计费映射哈希字段或服务映射",description="编辑计费映射哈希字段或服务映射")
async def edit_rating_module_config_hashmap_mappings(mapping_id: str, mapping: RatingModuleConfigHashMapMapping):
    try:
        return cloudkitty_service.edit_rating_module_config_hashmap_mappings(mapping_id, mapping)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail={e})

@router.put("/cloudkitty/module_config/hashmap/thresholds/{threshold_id}", summary="编辑计费映射哈希服务阈值",description="编辑计费映射哈希服务阈值")
async def edit_rating_module_config_hashmap_thresholdings(threshold_id: str, thresholding: RatingModuleConfigHashMapThreshold):
    try:
        return cloudkitty_service.edit_rating_module_config_hashmap_thresholdings(threshold_id, thresholding)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail={e})

@router.put("/cloudkitty/modules/{module_id}", summary="编辑计费模型（禁用/启用模块、优先级）",description="编辑计费模型（禁用/启用模块、优先级）")
async def edit_rating_module_modules(module_id: str, modules: RatingModules):
    try:
        return cloudkitty_service.edit_rating_module_modules(module_id, modules)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail={e})



