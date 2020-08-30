# 各種ライブラリインポート
import bpy

# 指定オブジェクトを複製する
def duplicate_object_target(arg_object:bpy.types.Object) -> bpy.types.Object:
    """指定オブジェクトを複製する

    Args:
        arg_object (bpy.types.Object): 指定オブジェクト

    Returns:
        bpy.types.Object: 複製オブジェクトの参照
    """

    # オブジェクトを複製する
    duplicatob = arg_object.copy()

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

