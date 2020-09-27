# 各種ライブラリインポート
import bpy

# 指定オブジェクトを複製して複製元の名称を付けるなどの設定を行う
def setting_object_duplicate(arg_object:bpy.types.Object) -> bpy.types.Object:
    """指定オブジェクトを複製して複製元の名称を付けるなどの設定を行う

    Args:
        arg_object (bpy.types.Object): 複製元オブジェクト

    Returns:
        bpy.types.Object: 複製オブジェクトの参照
    """

    # 指定オブジェクトが存在するか確認する
    if arg_object == None:
        # 指定オブジェクトが存在しない場合は処理しない
        return None
    
    # オブジェクトがメッシュであるか確認する
    if arg_object.type != 'MESH':
        # 指定オブジェクトがメッシュでない場合は処理しない
        return None
        
    # 対象オブジェクトを複製する
    duplicate_object = singlecopy_object_target(arg_object=arg_object)

    # 複製元オブジェクトの名前を取得する
    base_name = arg_object.name

    # 複製元オブジェクトの名前を変更する
    arg_object.name = base_name + "_base"

    # 複製オブジェクトに複製元オブジェクトの名前を設定する
    duplicate_object.name = base_name

    return duplicate_object

# 指定オブジェクトを複製してシングルユーザ化する
def singlecopy_object_target(arg_object:bpy.types.Object) -> bpy.types.Object:
    """指定オブジェクトをしてシングルユーザ化する

    Args:
        arg_object (bpy.types.Object): 指定オブジェクト

    Returns:
        bpy.types.Object: 複製オブジェクトの参照
    """

    # オブジェクトを複製する
    duplicatob = arg_object.copy()

    # オブジェクトのメッシュデータを取得する
    # IDアクセスのマニュアル
    # (https://docs.blender.org/api/current/bpy.types.ID.html)
    mesh = duplicatob.data
    
    # メッシュの参照ユーザ数を取得する
    user_count = mesh.users

    # 複数のユーザが参照しているか確認する
    if user_count > 1:
        # シングルユーザ化するため、メッシュのコピーを作成して参照する
        duplicatob.data = mesh.copy()

    # 複製先のコレクションの参照
    target_collection = None

    # 全てのコレクションを操作する
    for collection in bpy.data.collections:
        # コレクション内に複製元オブジェクトが含まれるか確認する
        if arg_object.name in collection.objects:
            # 複製元オブジェクトのコレクションを複製先とする
            target_collection = collection

    # 複製先のコレクションが存在するか確認する
    if target_collection != None:
        # 複製したオブジェクトをシーンの複製先コレクションにリンクする
        target_collection.objects.link(duplicatob)
    else:
        # 複製先のコレクションが見つからない場合はコンテキストにリンクする
        bpy.context.scene.collection.objects.link(duplicatob)

    return duplicatob

