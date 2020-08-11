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

    # 不要なオブジェクトを選択しないように
    # 全てのオブジェクトを走査する
    for ob in bpy.context.scene.objects:
        # 非選択状態に設定する
        ob.select_set(False)
    
    # オブジェクトを選択状態にする
    arg_object.select_set(True)

    # オブジェクトを複製する
    bpy.ops.object.duplicate_move()

    # 複製オブジェクトを取得する
    duplicatob = bpy.context.scene.objects[-1]
    
    return duplicatob

