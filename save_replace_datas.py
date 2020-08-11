# bpyインポート
import bpy

# 指定オブジェクトのマテリアルを指定テクスチャのシンプルなプリンシプルBSDFマテリアルのみとする
def replace_material_textureBSDF(arg_object:bpy.types.Object, arg_texture:bpy.types.Image) -> bool:
    """[summary]

    Args:
        arg_object (bpy.types.Object): [description]
        arg_texture (bpy.types.Image): [description]

    Returns:
        bool: [description]
    """

    # 指定オブジェクトの全マテリアルを削除する
    is_alldel = delete_material_all(arg_object=arg_object)

    # 実行正否を確認する
    if is_alldel == False:
        # 削除に失敗した場合は処理しない
        return False

    # 指定テクスチャを参照するシンプルなBSDFマテリアルを作成する
    texture_mat = add_material_textureBSDF(arg_object=arg_object, arg_texture=arg_texture)

    # マテリアルを作成できたか確認する
    if texture_mat == None:
        # 作成に失敗した場合は実行失敗を返す
        return False
    
    return True

# 指定オブジェクトのマテリアルを全て削除する
def delete_material_all(arg_object:bpy.types.Object) -> bool:
    """指定オブジェクトのマテリアルを全て削除する

    Args:
        arg_object (bpy.types.Object): 指定オブジェクト
        arg_materialname (str, optional): 作成マテリアル名. Defaults to "DefaultMaterial".

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

    # メッシュのマテリアルを全て削除する
    while len(meshdata.materials) > 0:

        # IDMaterial操作のマニュアル
        # (https://docs.blender.org/api/current/bpy.types.IDMaterials.html)
        meshdata.materials.pop(index=-1)

    return True

# 指定オブジェクトに指定テクスチャのシンプルなプリンシプルBSDFマテリアルを作成する
def add_material_textureBSDF(arg_object:bpy.types.Object, arg_texture:bpy.types.Image) -> bpy.types.Material:
    """指定オブジェクトに指定テクスチャのシンプルなプリンシプルBSDFマテリアルを作成する

    Args:
        arg_object (bpy.types.Object): 指定オブジェクト
        arg_texture (bpy.types.Image): 指定テクスチャ

    Returns:
        bpy.types.Material: 作成マテリアルの参照
    """

    # 新規マテリアルを作成する
    new_material = bpy.data.materials.new("TextureMaterial")

    # メッシュデータの参照を取得する
    meshdata = arg_object.data

    # メッシュのマテリアルを追加する
    meshdata.materials.append(new_material)

    # 追加したマテリアルスロットを取得する
    add_matslot = arg_object.material_slots[-1]

    # ノードを使用する
    new_material.use_nodes = True

    # 新規マテリアルのノード参照を取得する
    mat_nodes = new_material.node_tree.nodes

    # マテリアル内の全ノードを走査する
    for delete_node in mat_nodes:
        # 一旦全てのノードを削除する
        mat_nodes.remove(delete_node)

    # テクスチャノードの追加
    texture_node = mat_nodes.new(type='ShaderNodeTexImage')

    # テクスチャノードに新規画像を設定する
    texture_node.image = arg_texture

    # プリンシプルBSDFノードを追加する
    bsdf_node = mat_nodes.new(type='ShaderNodeBsdfPrincipled')

    # 出力ノードを追加する
    output_node = mat_nodes.new(type='ShaderNodeOutputMaterial')

    # ターゲットマテリアルのノードリンク参照を取得する
    mat_link = new_material.node_tree.links

    # テクスチャノードのカラーとプリンシプルBSDFノードのベースカラーを接続する
    mat_link.new(texture_node.outputs[0], bsdf_node.inputs[0])
    
    # プリンシプルBSDFのシェーダ出力と出力ノードのサーフェスを接続する
    mat_link.new(bsdf_node.outputs[0], output_node.inputs[0])

    return new_material

# 指定ディレクトリにテクスチャをPNG形式で保存する
def save_image_targetdir(arg_image:bpy.types.Image, arg_directory:str,
  arg_colormode:str='RGBA', arg_colordepth:str='8', arg_compression:int=15) -> bool:
    """指定ディレクトリにテクスチャをPNG形式で保存する

    Args:
        arg_image (bpy.types.Image): 保存テクスチャ
        arg_directory (str): 指定ディレクトリ
        arg_colormode (str, optional): カラーモード指定. Defaults to 'RGBA'.
        arg_colordepth (str, optional): 色深度指定. Defaults to '8'.
        arg_compression (int, optional): 圧縮率指定. Defaults to 15.

    Returns:
        bool: 実行正否
    """

    # 保存ファイルパスを作成する
    savepath = arg_directory + "\\" + arg_image.name + ".png"

    # 保存ファイルパスを指定する
    arg_image.filepath_raw = savepath

    # ファイルフォーマットをPNGに設定する
    arg_image.file_format = 'PNG'

    # レンダー色空間で保存するためのシーンを取得する
    # (https://docs.blender.org/api/current/bpy.types.Scene.html)
    render_scene = bpy.context.scene

    # 現在のカラーマネジメントのビュー変換を取得する
    current_view_transform = render_scene.view_settings.view_transform

    # カラーマネジメントのビュー変換を[標準]に設定する（Filmicだと灰色に出力されるため）
    # (https://docs.blender.org/api/current/bpy.types.ColorManagedViewSettings.html)
    render_scene.view_settings.view_transform = 'Standard'

    # シーンのレンダリング設定からイメージフォーマット設定の参照を取得する
    scene_imagesettings = render_scene.render.image_settings

    # カラーフォーマットを設定する
    scene_imagesettings.color_mode = arg_colormode

    # 色深度を設定する
    scene_imagesettings.color_depth = arg_colordepth

    # 圧縮率を設定する
    scene_imagesettings.compression = arg_compression

    # シーンのレンダリング設定を利用して画像を保存する
    arg_image.save_render(filepath=savepath, scene=render_scene)

    # 変更したビュー変換を元に戻す
    render_scene.view_settings.view_transform = current_view_transform

    return True

