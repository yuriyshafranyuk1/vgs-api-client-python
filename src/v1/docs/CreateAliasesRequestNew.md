# CreateAliasesRequestNew


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**format** | [**AliasFormat**](AliasFormat.md) |  | 
**value** | **str** | Raw value to encrypt &amp; store in the vault. | 
**classifiers** | **[str]** | List of tags to classify the value with. | [optional] 
**storage** | **str** | Storage medium to use.  VOLATILE results in data being persisted into an in-memory data store for one hour which is required for PCI compliant storage of card security code data.  | [optional]  if omitted the server will use the default value of "PERSISTENT"
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


