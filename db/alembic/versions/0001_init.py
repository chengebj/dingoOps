# 运维模块的数据库初始化脚本

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ops_assets",
        sa.Column("uuid", sa.String(length=128), nullable=False),
        sa.Column("asset_name", sa.String(length=128), nullable=True),
        sa.Column("asset_description", sa.String(length=255), nullable=True),
    )
    op.create_index(op.f("ix_ops_assets_uuid"), "ops_assets", ["uuid"], unique=False)
    # ### end Alembic commands ###

    # ### 资产类型信息 ###
    assets_types_table = op.create_table(
        "ops_assets_types",
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("parent_id", sa.String(length=128), nullable=True),
        sa.Column("asset_type_name", sa.String(length=128), nullable=True),
        sa.Column("asset_type_name_zh", sa.String(length=128), nullable=True),
        sa.Column("queue", sa.Integer(), nullable=False, default=0),
        sa.Column("description", sa.String(length=255), nullable=True),
    )
    op.create_index(op.f("ix_ops_assets_types_id"), "ops_assets_types", ["id"], unique=False)
    # ### 资产类型初始化信息 ###
    op.bulk_insert(assets_types_table,
                   [
                       {'id':'603d61bb-be7b-11ef-90c8-44a842237864', 'parent_id': None, 'asset_type_name':'PART', 'asset_type_name_zh':'配件', 'queue':3, 'description':None},
                       {'id':'8fb707d8-b07e-11ef-90c8-44a842237864', 'parent_id': None, 'asset_type_name':'SERVER', 'asset_type_name_zh':'服务器', 'queue':1, 'description':None},
                       {'id':'8fbc77f1-b07e-11ef-90c8-44a842237864', 'parent_id': None, 'asset_type_name':'NETWORK', 'asset_type_name_zh':'网络设备', 'queue':2, 'description':None}
                   ]
                   )

    # ### 资产基础信息 ###
    op.create_table(
        "ops_assets_basic_info",
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("asset_type_id", sa.String(length=128), nullable=True),
        sa.Column("asset_category", sa.String(length=128), nullable=True),
        sa.Column("asset_type", sa.String(length=128), nullable=True),
        sa.Column("name", sa.String(length=128), nullable=True),
        sa.Column("equipment_number", sa.String(length=128), nullable=True),
        sa.Column("sn_number", sa.String(length=128), nullable=True),
        sa.Column("asset_number", sa.String(length=128), nullable=True),
        sa.Column("asset_status", sa.String(length=40), nullable=True),
        sa.Column("asset_status_description", sa.Text(), nullable=True),
        sa.Column("extra", sa.Text(), nullable=True),
        sa.Column("extend_column_extra", sa.Text(), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
    )
    op.create_index(op.f("ix_ops_assets_basic_info_id"), "ops_assets_basic_info", ["id"], unique=False)

    # ### 资产配件信息 ###
    op.create_table(
        "ops_assets_parts_info",
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("asset_id", sa.String(length=128), nullable=True),
        sa.Column("part_type", sa.String(length=128), nullable=True),
        sa.Column("part_brand", sa.String(length=128), nullable=True),
        sa.Column("part_config", sa.String(length=128), nullable=True),
        sa.Column("part_number", sa.String(length=128), nullable=True),
        sa.Column("personal_used_flag", sa.Boolean(), nullable=True),
        sa.Column("surplus", sa.String(length=128), nullable=True),
        sa.Column("name", sa.String(length=128), nullable=True),
        sa.Column("extra", sa.Text(), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
    )
    op.create_index(op.f("ix_ops_assets_manufactures_info_id"), "ops_assets_manufactures_info", ["id"], unique=False)

    # ### 资产厂商信息 ###
    op.create_table(
        "ops_assets_manufactures_info",
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("asset_id", sa.String(length=128), nullable=True),
        sa.Column("name", sa.String(length=128), nullable=True),
        sa.Column("extra", sa.Text(), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
    )
    op.create_index(op.f("ix_ops_assets_manufactures_info_id"), "ops_assets_manufactures_info", ["id"], unique=False)

    # ### 资产厂商关联关系信息 ###
    op.create_table(
        "ops_assets_manufactures_relations_info",
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("asset_id", sa.String(length=128), nullable=True),
        sa.Column("manufacture_id", sa.String(length=128), nullable=True),
    )
    op.create_index(op.f("ix_ops_assets_manufactures_relations_info_id"), "ops_assets_manufactures_relations_info", ["id"], unique=False)

    # ### 资产位置信息 ###
    op.create_table(
        "ops_assets_positions_info",
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("asset_id", sa.String(length=128), nullable=True),
        sa.Column("frame_position", sa.String(length=128), nullable=True),
        sa.Column("cabinet_position", sa.String(length=128), nullable=True),
        sa.Column("u_position", sa.String(length=128), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
    )
    op.create_index(op.f("ix_ops_assets_positions_info_id"), "ops_assets_positions_info", ["id"], unique=False)

    # ### 资产合同信息 ###
    op.create_table(
        "ops_assets_contracts_info",
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("asset_id", sa.String(length=128), nullable=True),
        sa.Column("contract_number", sa.String(length=128), nullable=True),
        sa.Column("purchase_date", sa.DateTime(), nullable=True),
        sa.Column("batch_number", sa.String(length=10), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
    )
    op.create_index(op.f("ix_ops_assets_contracts_info_id"), "ops_assets_contracts_info", ["id"], unique=False)

    # ### 资产归属用户信息 ###
    op.create_table(
        "ops_assets_belongs_info",
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("asset_id", sa.String(length=128), nullable=True),
        sa.Column("department_id", sa.String(length=128), nullable=True),
        sa.Column("department_name", sa.String(length=128), nullable=True),
        sa.Column("user_id", sa.String(length=128), nullable=True),
        sa.Column("user_name", sa.String(length=128), nullable=True),
        sa.Column("tel_number", sa.String(length=128), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
    )
    op.create_index(op.f("ix_ops_assets_belongs_info_id"), "ops_assets_belongs_info", ["id"], unique=False)

    # ### 资产租赁客户信息 ###
    op.create_table(
        "ops_assets_customers_info",
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("asset_id", sa.String(length=128), nullable=True),
        sa.Column("customer_id", sa.String(length=128), nullable=True),
        sa.Column("customer_name", sa.String(length=128), nullable=True),
        sa.Column("rental_duration", sa.Integer(), nullable=True),
        sa.Column("start_date", sa.DateTime(), nullable=True),
        sa.Column("end_date", sa.DateTime(), nullable=True),
        sa.Column("vlan_id", sa.String(length=128), nullable=True),
        sa.Column("float_ip", sa.String(length=128), nullable=True),
        sa.Column("band_width", sa.String(length=128), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
    )
    op.create_index(op.f("ix_ops_assets_customers_info_id"), "ops_assets_customers_info", ["id"], unique=False)

    # ### 资产设备的流入流出信息 ###
    op.create_table(
        "ops_assets_flows_info",
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("asset_id", sa.String(length=128), nullable=True),
        sa.Column("port", sa.String(length=128), nullable=True),
        sa.Column("label", sa.String(length=255), nullable=True),
        sa.Column("opposite_asset_id", sa.String(length=128), nullable=True),
        sa.Column("opposite_port", sa.String(length=128), nullable=True),
        sa.Column("opposite_label", sa.String(length=255), nullable=True),
        sa.Column("cable_type", sa.String(length=128), nullable=True),
        sa.Column("cable_interface_type", sa.String(length=128), nullable=True),
        sa.Column("cable_length", sa.Integer(), nullable=True),
        sa.Column("extra", sa.Text(), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
    )
    op.create_index(op.f("ix_ops_assets_flows_info_id"), "ops_assets_flows_info", ["id"], unique=False)

    # ### 资产设备的扩展字段信息 ###
    op.create_table(
        "ops_assets_extends_columns_info",
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("asset_type", sa.String(length=128), nullable=True),
        sa.Column("role_type", sa.String(length=128), nullable=True),
        sa.Column("column_key", sa.String(length=128), nullable=True),
        sa.Column("column_name", sa.String(length=128), nullable=True),
        sa.Column("column_type", sa.String(length=128), nullable=True),
        sa.Column("required_flag", sa.Boolean(), nullable=True),
        sa.Column("default_flag", sa.Boolean(), nullable=True),
        sa.Column("hidden_flag", sa.Boolean(), nullable=True),
        sa.Column("queue", sa.Integer(), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
    )
    op.create_index(op.f("ix_ops_assets_extends_columns_info_id"), "ops_assets_extends_columns_info", ["id"], unique=False)

    # ### 操作日志信息 ###
    op.create_table(
        "ops_operate_log",
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("log_date", sa.DateTime(), nullable=True),
        sa.Column("user_id", sa.String(length=128), nullable=True),
        sa.Column("user_name", sa.String(length=128), nullable=True),
        sa.Column("ip", sa.String(length=128), nullable=True),
        sa.Column("operate_type", sa.String(length=128), nullable=True),
        sa.Column("resource_type", sa.String(length=128), nullable=True),
        sa.Column("resource_type_name", sa.String(length=128), nullable=True),
        sa.Column("resource_id", sa.String(length=128), nullable=True),
        sa.Column("resource_name", sa.String(length=128), nullable=True),
        sa.Column("operate_flag", sa.Boolean(), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
    )
    op.create_index(op.f("ix_ops_operate_log_id"), "ops_operate_log", ["id"], unique=False)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_ops_assets_uuid"), table_name="ops_assets")
    op.drop_table("ops_assets")
    # ### end Alembic commands ###
