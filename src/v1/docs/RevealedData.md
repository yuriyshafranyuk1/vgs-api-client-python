# RevealedData


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**aliases** | [**[Alias]**](Alias.md) | List of aliases associated with the value. | [optional] 
**classifiers** | **[str]** | List of tags the value is classified with. | [optional] 
**created_at** | **datetime** | Creation time, in UTC. | [optional] 
**storage** | **str** | Storage medium to use.  VOLATILE results in data being persisted into an in-memory data store for one hour which is required for PCI compliant storage of card security code data.  | [optional]  if omitted the server will use the default value of "PERSISTENT"
**value** | **str** | Decrypted value stored in the vault. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


