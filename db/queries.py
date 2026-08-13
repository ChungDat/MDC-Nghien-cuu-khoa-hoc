import toml
from supabase import create_client, Client

secrets = toml.load(".streamlit/secrets.toml")
url = secrets["connections"]["supabase"]["SUPABASE_URL"]
key = secrets["connections"]["supabase"]["SUPABASE_KEY"]

conn: Client = create_client(url, key)

def get_form(id) -> dict[str, int]:
    """
    Lấy một dòng dữ liệu từ bảng forms

    Parameters:
        id (str): ID của form

    Returns:
        dict: Dữ liệu của form
    """
    return conn.table("forms").select("*").eq("id", id).execute().data

def get_prediction(form_id) -> dict[str, int]:
    """
    Lấy một dòng dữ liệu từ bảng predictions

    Parameters:
        form_id (str): ID của form

    Returns:
        dict: Dữ liệu của prediction
    """
    return conn.table("predictions").select("*").eq("form_id", id).execute().data

def get_all_forms() -> list[dict[str, int]]:
    """
    Lấy tất cả dòng dữ liệu từ bảng forms

    Returns:
        dict: Tất cả dữ liệu của form
    """
    return conn.table("forms").select("*").execute().data

def get_all_predictions() -> list[dict[str, int]]:
    """
    Lấy tất cả dòng dữ liệu từ bảng predictions

    Returns:
        dict: Tất cả dữ liệu của prediction
    """
    return conn.table("predictions").select("*").execute().data

def get_all() -> list[dict[str, int]]:
    return conn.table("forms").select("*, predictions(*)").execute().data

def add_form(data: dict[str, int]) -> str:
    """
    Thêm một dòng vào bảng forms
    
    Parameters:
        data (dict): Dữ liệu cần thêm ({'cb_01': 1, 'cb_02': 3, ...})

    Returns:
        str: ID của form vừa được thêm
    """
    return conn.table("forms").insert([data]).execute().data[0]["id"]

def add_prediction(form_id: str, data: dict[str, int]) -> None:
    """
    Thêm một dòng vào bảng predictions
    
    Parameters:
        form_id (str): ID của form
        data (dict): Dữ liệu cần thêm ({'pais_01': 1, 'pais_02': 3, ...})
    """
    result = [{"form_id": form_id, **data}]
    conn.table("predictions").insert(result).execute()

def remove_form(id) -> None:
    """
    Xoá một dòng trong bảng forms và predictions

    Parameters:
        id (str): ID của form

    Returns:
        dict: Dữ liệu đã xoá
    """
    conn.table("forms").delete().eq("id", id).execute()
    conn.table("predictions").delete().eq("form_id", id).execute()