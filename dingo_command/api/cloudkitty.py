# 计费的api接口
import os
from typing import List

from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from dingo_command.api.model.cloudkitty import CloudKittyRatingSummaryDetail
from dingo_command.services.cloudkitty import CloudKittyService
from dingo_command.utils import file_utils

from dingo_command.utils.constant import EXCEL_TEMP_DIR
from dingo_command.utils.datetime import format_d8q_timestamp
from fastapi import APIRouter, HTTPException, Query

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

@router.post("/cloudkitty/download/ratingSummaryDetail/pdf", summary="下载计费汇总详情PDF", description="下载计费汇总详情PDF")
async def download_rating_summary_detail_pdf(detail: List[CloudKittyRatingSummaryDetail],
                                             language: str = Query(None, description="当前环境语言")):
    result_file_pdf_name = "rating_summary_detail_" + format_d8q_timestamp() + ".pdf"
    # 导出文件路径
    result_file_pdf_path = EXCEL_TEMP_DIR + result_file_pdf_name

    # 1. 生成PDF文件
    try:
        cloudkitty_service.download_rating_summary_detail_pdf(result_file_pdf_path, detail, language)
    except Exception as e:
        import traceback
        traceback.print_exc()
        file_utils.cleanup_temp_file(result_file_pdf_path)
        raise HTTPException(status_code=400, detail="generate pdf file error")

    # 文件存在则下载
    if os.path.exists(result_file_pdf_path):
        return FileResponse(
            path=result_file_pdf_path,
            media_type="application/octet-stream",
            filename=result_file_pdf_name,  # 下载时显示的文件名
            background=BackgroundTask(file_utils.cleanup_temp_file, result_file_pdf_path)
        )
    raise HTTPException(status_code=400, detail="PDf file not found")

@router.post("/cloudkitty/download/ratingSummaryDetail/execl", summary="下载计费汇总详情execl", description="下载计费汇总详情execl")
async def download_rating_summary_detail_execl(detail: List[CloudKittyRatingSummaryDetail],
                                             language: str = Query(None, description="当前环境语言")):
    result_file_execl_name = "rating_summary_detail_" + format_d8q_timestamp() + ".xlsx"
    # 导出文件路径
    result_file_execl_path = EXCEL_TEMP_DIR + result_file_execl_name

    # 1. 生成Excel文件
    try:
        cloudkitty_service.download_rating_summary_detail_execl(result_file_execl_path, detail, language)
    except Exception as e:
        import traceback
        traceback.print_exc()
        file_utils.cleanup_temp_file(result_file_execl_path)
        raise HTTPException(status_code=400, detail="generate execl file error")

    # 文件存在则下载
    if os.path.exists(result_file_execl_path):
        return FileResponse(
            path=result_file_execl_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=result_file_execl_name,  # 下载时显示的文件名
            background=BackgroundTask(file_utils.cleanup_temp_file, result_file_execl_path)
        )
    raise HTTPException(status_code=400, detail="Execl file not found")


