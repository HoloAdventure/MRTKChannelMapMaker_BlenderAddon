# 各種ライブラリインポート
import bpy

# レンダリング時に有効なUVマップレイヤーを取得する
# 既存のUVマップレイヤーがない場合はスマートUV展開で作成する
def get_uvlayer(arg_object:bpy.types.Object) -> bpy.types.MeshUVLoopLayer:
    """レンダリング時に有効なUVマップレイヤーを取得する
    既存のUVマップレイヤーがない場合はスマートUV展開で作成する

    Args:
        arg_object (bpy.types.Object): 指定オブジェクト

    Returns:
        bpy.types.MeshUVLoopLayer: UVマップレイヤーの参照
    """
    
    # UVマップが存在するか確認する
    ret_uvlayer = get_uvlayer_active(arg_object=arg_object)
    if ret_uvlayer == None:
        # UVマップが存在しない場合はスマートUV展開を実行する
        ret_uvlayer = project_uv_smart(arg_object=arg_object)
    
    return ret_uvlayer

# レンダリング時に有効なUVマップレイヤーを取得する
def get_uvlayer_active(arg_object:bpy.types.Object) -> bpy.types.MeshUVLoopLayer:
    """レンダリング時に有効なUVマップレイヤーを取得する

    Args:
        arg_object (bpy.types.Object): 指定オブジェクト

    Returns:
        bpy.types.MeshUVLoopLayer: 有効なUVマップレイヤーの参照
    """

    # 指定オブジェクトがメッシュオブジェクトか確認する
    if arg_object.type != 'MESH':
        # メッシュオブジェクトでない場合は処理しない
        return False

    # 対象オブジェクトのメッシュデータを取得する
    # メッシュデータ操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.Mesh.html)
    meshdata = arg_object.data

    # UVマップレイヤーのリストを取得する
    # UVマップレイヤーのリスト操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.UVLoopLayers.html)
    uv_layers = meshdata.uv_layers

    # アクティブなUVマップを取得する
    # UVマップレイヤー操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.MeshUVLoopLayer.html)
    active_uvlayer = uv_layers.active

    return active_uvlayer

# 指定オブジェクトのUVマップレイヤーを全て削除する
def delete_uvlayer_all(arg_object:bpy.types.Object) -> bool:
    """指定オブジェクトのUVマップレイヤーを全て削除する

    Args:
        arg_object (bpy.types.Object): 指定オブジェクト

    Returns:
        bool: 実行正否
    """

    # 指定オブジェクトがメッシュオブジェクトか確認する
    if arg_object.type != 'MESH':
        # メッシュオブジェクトでない場合は処理しない
        return False

    # 対象オブジェクトのメッシュデータを取得する
    # メッシュデータ操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.Mesh.html)
    meshdata = arg_object.data

    # UVマップレイヤーのリストを取得する
    # UVマップレイヤーのリスト操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.UVLoopLayers.html)
    uv_layers = meshdata.uv_layers

    # UVマップレイヤーを全て走査する
    for uv_layer in uv_layers:
        # UVマップレイヤーを全て削除する
        uv_layers.remove(uv_layer)
    
    return

# 通常のUV展開を実行する
def project_uv_normal(arg_object:bpy.types.Object) -> bpy.types.MeshUVLoopLayer:
    """通常のUV展開を実行する

    Args:
        arg_object (bpy.types.Object): 指定オブジェクト

    Returns:
        bpy.types.MeshUVLoopLayer: 作成UVマップレイヤーの参照
    """

    # 不要なオブジェクトを選択しないように
    # 全てのオブジェクトを走査する
    for ob in bpy.context.scene.objects:
        # 非選択状態に設定する
        ob.select_set(False)
    
    # オブジェクトを選択状態にする
    arg_object.select_set(True)
 
    # 編集モードに移行する
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    
    # 頂点を全選択した状態とする
    bpy.ops.mesh.select_all(action='SELECT')
    
    # 通常のUV展開を実行する
    # 方式：アングルベース,穴を埋める：True,アスペクト比の補正：True,
    # 細分化モディファイアを使用：False,余白:0.1
    bpy.ops.uv.unwrap(method='ANGLE_BASED', fill_holes=True,
      correct_aspect=True, use_subsurf_data=False, margin=0.1)
    
    # オブジェクトモードに移行する
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    
    # 対象オブジェクトに追加されたUVマップを取得する
    active_uvlayer = arg_object.data.uv_layers[-1]
    
    return active_uvlayer

# スマートUV展開を実行する
def project_uv_smart(arg_object:bpy.types.Object) -> bpy.types.MeshUVLoopLayer:
    """スマートUV展開を実行する

    Args:
        arg_object (bpy.types.Object): 指定オブジェクト

    Returns:
        bpy.types.MeshUVLoopLayer: 作成UVマップレイヤーの参照
    """

    # 不要なオブジェクトを選択しないように
    # 全てのオブジェクトを走査する
    for ob in bpy.context.scene.objects:
        # 非選択状態に設定する
        ob.select_set(False)
    
    # オブジェクトを選択状態にする
    arg_object.select_set(True)
 
    # 編集モードに移行する
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    
    # 頂点を全選択した状態とする
    bpy.ops.mesh.select_all(action='SELECT')
    
    # スマートUV展開を実行する
    # 角度制限：66,島の余白：0.1,エリアウェイト：0,アスペクト比の補正：True,UV境界に合わせる：True
    bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.1,
      user_area_weight=0, use_aspect=True, stretch_to_bounds=True)
    
    # オブジェクトモードに移行する
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    
    # 対象オブジェクトに追加されたUVマップを取得する
    active_uvlayer = arg_object.data.uv_layers[-1]
    
    return active_uvlayer

