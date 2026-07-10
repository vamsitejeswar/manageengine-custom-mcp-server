from typing import Optional
from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from src.api.client import me_client
from src.api.endpoints import CustomField

_R = ToolAnnotations(readOnlyHint=True)
_W = ToolAnnotations(readOnlyHint=False, destructiveHint=True)


def register_custom_field_tools(mcp: FastMCP) -> None:

    @mcp.tool(annotations=_R)
    async def cf_get_udt_length(actualColumnName: str, tableName: str) -> dict:
        """Fetch the maximum allowed length for a user-defined data type (UDT) column."""
        return await me_client.get(CustomField.UDT_LENGTH, params={
            "actualColumnName": actualColumnName,
            "tableName": tableName,
        })

    @mcp.tool(annotations=_R)
    async def cf_list() -> dict:
        """Fetch the list of all custom field definitions."""
        return await me_client.get(CustomField.LIST)

    @mcp.tool(annotations=_W)
    async def cf_create(
        columnName: str,
        dataType: str,
        tableName: str,
        size: int | None = None,
        defaultValue: str | None = None,
        description: str | None = None,
        isPII: bool | None = None,
    ) -> dict:
        """Add a new custom field column."""
        body = {k: v for k, v in {
            "columnName": columnName,
            "dataType": dataType,
            "tableName": tableName,
            "size": size,
            "defaultValue": defaultValue,
            "description": description,
            "isPII": isPII,
        }.items() if v is not None}
        return await me_client.post(CustomField.ADD, json=body)

    @mcp.tool(annotations=_W)
    async def cf_update(
        actualColumnName: str,
        dataType: str,
        tableName: str,
        size: int | None = None,
        defaultValue: str | None = None,
        description: str | None = None,
        isPII: bool | None = None,
        forceUpdate: bool | None = None,
    ) -> dict:
        """Update an existing custom field column definition."""
        body = {k: v for k, v in {
            "actualColumnName": actualColumnName,
            "dataType": dataType,
            "tableName": tableName,
            "size": size,
            "defaultValue": defaultValue,
            "description": description,
            "isPII": isPII,
        }.items() if v is not None}
        params = {"forceUpdate": forceUpdate} if forceUpdate is not None else None
        return await me_client.put(CustomField.MODIFY, json=body, params=params)

    @mcp.tool(annotations=_W)
    async def cf_update_value(
        actualColumnName: str,
        tableName: str,
        customColumnValue: str | None = None,
        resourceName: str | None = None,
        selectedResources: list[str] | None = None,
    ) -> dict:
        """Modify a custom column value for selected resources."""
        body = {k: v for k, v in {
            "actualColumnName": actualColumnName,
            "tableName": tableName,
            "customColumnValue": customColumnValue,
            "resourceName": resourceName,
            "selectedResources": selectedResources,
        }.items() if v is not None}
        return await me_client.put(CustomField.MODIFY_VALUE, json=body)

    @mcp.tool(annotations=_W)
    async def cf_delete(
        actualColumnName: str,
        tableName: str,
        forceDelete: bool | None = None,
    ) -> dict:
        """Delete a custom field column."""
        params = {"forceDelete": forceDelete} if forceDelete is not None else None
        return await me_client.delete(
            CustomField.REMOVE,
            json={"actualColumnName": actualColumnName, "tableName": tableName},
            params=params,
        )

    @mcp.tool(annotations=_W)
    async def cf_create_data_type(
        dataType: str,
        baseType: str,
        allowedValues: list[str] | None = None,
        size: int | None = None,
        defaultValue: str | None = None,
    ) -> dict:
        """Create a custom data type for use in custom fields."""
        body = {k: v for k, v in {
            "dataType": dataType,
            "baseType": baseType,
            "allowedValues": allowedValues,
            "size": size,
            "defaultValue": defaultValue,
        }.items() if v is not None}
        return await me_client.post(CustomField.DATA_TYPE, json=body)

    @mcp.tool(annotations=_R)
    async def cf_check_udt_name_exists(udtName: str) -> dict:
        """Check whether a user-defined data type name already exists."""
        return await me_client.get(CustomField.UDT_NAME_EXISTS, params={"udtName": udtName})

    @mcp.tool(annotations=_W)
    async def cf_update_computer_value(resource_id: str, uem_safestring: str) -> dict:
        """Update the value of a custom field for a specific computer (resource ID)."""
        return await me_client.post(
            CustomField.computer_update(resource_id),
            json={"uem_safestring": uem_safestring},
        )

    @mcp.tool(annotations=_R)
    async def cf_get_computer_fields(resource_id: str) -> dict:
        """Fetch the list of custom fields for a specific resource (computer or software)."""
        return await me_client.get(CustomField.computer_fields(resource_id))

    @mcp.tool(annotations=_R)
    async def cf_get_computer_metadata(resource_id: str) -> dict:
        """Fetch custom field metadata for a specific computer by resource ID."""
        return await me_client.get(CustomField.computer_metadata(resource_id))
