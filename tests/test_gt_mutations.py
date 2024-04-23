import pytest

from .shared import prepare_in_memory_sqllite, prepare_demodata, createContext, get_demodata
from src.GraphTypeDefinitions import schema

@pytest.mark.asyncio
async def test_externalid_mutation():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    externalidtypestable = data["externalidtypes"]
    row = externalidtypestable[0]
    type_id = f"{row['id']}"

    userstable = data["users"]
    row = userstable[0]
    user_id = f"{row['id']}"

    query = '''
            mutation(
                $inner_id: UUID!
                $typeid_id: UUID!
                $outer_id: String!
            ) {
                result: externalidInsert(externalid: {
                    innerId: $inner_id
                    typeidId: $typeid_id
                    outerId: $outer_id
                }) {
                    id
                    msg
                    externalid {
                        id
                        innerId
                        outerId
                        type {
                            id
                        }
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {'inner_id': user_id, 'outer_id': '999', 'typeid_id': type_id}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    print(resp, flush=True)
    assert resp.errors is None, f"got errors {resp.errors}"
    
    respdata = resp.data["result"]
    assert respdata is not None, f"missing data {resp}"
    assert respdata["msg"] == "ok", f"something bad {resp}"
    assert respdata["externalid"]["outerId"] == "999", f"something bad {resp}"
    assert respdata["externalid"]["innerId"] == user_id, f"something bad {resp}"
    assert respdata["externalid"]["type"]["id"] == type_id, f"something bad {resp}"

    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    print(resp, flush=True)
    assert resp.errors is None
    
    respdata = resp.data["result"]
    assert respdata is not None
    assert respdata["msg"] == "fail", f"something bad {resp}"
    
# @pytest.mark.asyncio
# async def test_externalid_delete():
#     async_session_maker = await prepare_in_memory_sqllite()
#     await prepare_demodata(async_session_maker)

#     data = get_demodata()
#     externalidtypestable = data["externalidtypes"]
#     row = externalidtypestable[0]
#     type_id = f'{row["id"]}'

#     userstable = data["users"]
#     row = userstable[0]
#     user_id = f'{row["id"]}'

#     query = '''
#             mutation(
#                 $inner_id: UUID!
#                 $typeid_id: UUID!
#                 $outer_id: String!
#             ) {
#                 result: externalidInsert(externalid: {
#                     innerId: $inner_id
#                     typeidId: $typeid_id
#                     outerId: $outer_id
#                 }) {
#                     id
#                     msg
#                     externalid {
#                         id
#                         innerId
#                         outerId
#                         type {
#                             id
#                         }
#                     }
#                 }
#             }
#         '''

#     context_value = await createContext(async_session_maker)
#     variable_values = {'inner_id': user_id, 'outer_id': '999', 'typeid_id': type_id}
#     resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
#     print(resp, flush=True)
#     assert resp.errors is None
    
#     respdata = resp.data["result"]
#     assert respdata is not None
#     assert respdata["msg"] == "ok"
#     assert respdata["externalid"]["outerId"] == "999"
#     assert respdata["externalid"]["innerId"] == user_id
#     assert respdata["externalid"]["type"]["id"] == type_id

#     # idToDelete = respdata["externalid"]["id"]

#     query = '''
#         mutation($inner_id: UUID!
#                 $typeid_id: UUID!
#                 $outer_id: String!) 
#         {
#             result: externalidDelete(externalid: {
#                 innerId: $inner_id
#                 typeidId: $typeid_id
#                 outerId: $outer_id} 
#             ) {
#                 id
#                 msg
#             }
#         }
#         '''
    
#     resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
#     print(resp, flush=True)
#     assert resp.errors is None
    
#     respdata = resp.data["result"]
#     assert respdata is not None
#     assert respdata["msg"] == "ok"

# @pytest.mark.asyncio
# async def test_externalid_delete_fail():
#     async_session_maker = await prepare_in_memory_sqllite()
#     await prepare_demodata(async_session_maker)

#     query = '''
#         mutation($inner_id: UUID!
#                 $typeid_id: UUID!
#                 $outer_id: String!) 
#         {
#             result: externalidDelete(externalid: {
#                 innerId: $inner_id
#                 typeidId: $typeid_id
#                 outerId: $outer_id} 
#             ) {
#                 id
#                 msg
#             }
#         }
#         '''
    
#     context_value = await createContext(async_session_maker)
#     variable_values = {'inner_id': "bbfe7a3b-de51-4bde-92e8-357e4c9b2603", 'outer_id': '999', 'typeid_id': "7fd29b7f-2adf-42a6-a840-91ea37696728"}
#     resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
#     print(resp, flush=True)
#     assert resp.errors is None
    
#     respdata = resp.data["result"]
#     assert respdata is not None
#     assert respdata["msg"] == "fail"