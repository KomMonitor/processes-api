from openapi_client import ApiException


def get_missing_timestamps_error(missing_timestamps: list, resource_type: str) -> list[dict]:
    error_list = []
    for t in missing_timestamps:
        error_list.append(
            {
                "type": "missingTimestamp",
                "affectedResourceType": resource_type,
                "affectedDatasetId": t["id"],
                "affectedTimestamps": t["missingTimestamps"],
                "affectedSpatialUnitFeatures": [],
                "errorMessage": "Timestamps are missing for one or more input datasets"
            }
        )
    return error_list


def get_api_client_error(e: ApiException, dataset_id: str = None, resource_type: str = None) -> dict:
    return {
        "type": "dataManagementApiError",
        "affectedResourceType": resource_type,
        "dataManagementApiErrorCode": e.status,
        "affectedDatasetId": dataset_id,
        "affectedTimestamps": [],
        "affectedSpatialUnitFeatures": [],
        "errorMessage": e.data
    }

