# 各種ライブラリインポート
import bpy

# 指定オブジェクトの全てのマテリアルの粗さ情報を画像テクスチャにベイクする
def bake_roughness_texture(arg_object:bpy.types.Object,
  arg_texturename:str="BakeTexture",
  arg_texturesize:int=2048,
  arg_bakemargin:int=0) -> bpy.types.Image:
    """指定オブジェクトの全てのマテリアルの粗さ情報を画像テクスチャにベイクする

    Args:
        arg_object (bpy.types.Object): 指定オブジェクト
        arg_texturename (str, optional): 作成テクスチャ名. Defaults to "BakeTexture".
        arg_texturesize (int, optional): 作成テクスチャサイズ(px). Defaults to 2048.
        arg_bakemargin (int, optional): ベイク余白(px). Defaults to 0.

    Returns:
        bpy.types.Image: 作成テクスチャの参照
    """

    # 参照の保存用変数
    name_mapping = {}

    # 追加する画像ノード名を定義する
    texturenode_name = "ForBakeTextureNode"

    # 新規テクスチャを作成して参照を取得する
    bake_image = make_new_image(
        arg_texturename=arg_texturename,
        arg_texturesize=arg_texturesize
    )

    # 指定オブジェクトのマテリアルリストを取得する
    for material_slot in arg_object.material_slots:
        # スロットのマテリアルを取得する
        target_material = material_slot.material

        # マテリアルが割り当てられているか
        if target_material == None:
            continue

        # 新規テクスチャを参照する画像ノードを追加する
        add_node = add_node_image(
            arg_material=target_material,
            arg_image=bake_image
        )

        # 作成ノードの参照を保存する
        name_mapping[texturenode_name + target_material.name] = add_node

        # 指定の画像ノードを選択状態に設定する
        select_node_target(
            arg_material=target_material,
            arg_node=name_mapping[texturenode_name + target_material.name]
        )

    # 指定オブジェクトの「粗さ」をベイクする
    bake_roughness_only(
        arg_object=arg_object,
        arg_bakemargin=arg_bakemargin,
        arg_GPUuse=True
    )

    # 指定オブジェクトのマテリアルリストを取得する
    for material_slot in arg_object.material_slots:
        # スロットのマテリアルを取得する
        target_material = material_slot.material

        # マテリアルが割り当てられているか
        if target_material == None:
            continue

        # 追加した画像ノードを削除する
        delete_node_target(
            arg_material=target_material,
            arg_node=name_mapping[texturenode_name + target_material.name]
        )
    
    return bake_image


# 新規画像を作成する
def make_new_image(arg_texturename:str="BakeTexture",
  arg_texturesize:int=2048) -> bpy.types.Image:
    """新規画像を作成する

    Args:
        arg_texturename (str, optional): 作成テクスチャ名. Defaults to "BakeTexture".
        arg_texturesize (int, optional): 作成テクスチャサイズ. Defaults to 2048.

    Returns:
        bpy.types.Image: 作成画像の参照
    """

    # 新規画像を作成する
    newimage = bpy.data.images.new(
        name=arg_texturename,
        width=arg_texturesize,
        height=arg_texturesize,
        alpha=True
    )

    return newimage


# 対象マテリアルに指定テクスチャを参照する画像ノードを追加する
def add_node_image(arg_material:bpy.types.Material,
  arg_image:bpy.types.Image) -> bpy.types.Node:
    """対象マテリアルに指定テクスチャを参照する画像ノードを追加する

    Args:
        arg_material (bpy.types.Material): 対象マテリアル
        arg_image (bpy.types.Image): 指定テクスチャ

    Returns:
        bpy.types.Node: 作成ノードの参照
    """

    # ノード操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.Node.html)

    # ターゲットマテリアルのノード参照を取得
    mat_nodes = arg_material.node_tree.nodes

    # テクスチャノードの追加
    texture_node = mat_nodes.new(type="ShaderNodeTexImage")

    # テクスチャノードに指定画像を設定する
    texture_node.image = arg_image

    return texture_node


# 対象マテリアルの指定ノードのみを選択状態する
def select_node_target(arg_material:bpy.types.Material, arg_node:bpy.types.Node):
    """対象マテリアルの指定ノードのみを選択状態する

    Args:
        arg_material (bpy.types.Material): 対象マテリアル
        arg_node (bpy.types.Node): 指定ノード
    """

    # ノード操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.Node.html)
    # ノードリスト操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.Nodes.html)

    # ターゲットマテリアルのノード参照を取得
    mat_nodes = arg_material.node_tree.nodes

    # 全てのノードの選択状態を解除する
    for mat_node in mat_nodes:
        # 選択状態を解除する
        mat_node.select = False

    # 指定ノードを選択状態にする
    arg_node.select = True

    # 指定ノードをアクティブにする
    mat_nodes.active = arg_node

    return


# 指定オブジェクトの粗さ情報のみをベイクする
def bake_roughness_only(arg_object:bpy.types.Object,
  arg_bakemargin:int=0, arg_GPUuse:bool=False):
    """指定オブジェクトのカラー情報のみをベイクする

    Args:
        arg_object (bpy.types.Object): 指定オブジェクト
        arg_bakemargin (int, optional): ベイク余白. Defaults to 0.
        arg_GPUuse (bool, optional): GPU利用指定. Defaults to False.
    """

    # 全てのオブジェクトを非選択状態にする
    for obj in bpy.context.scene.objects:
        # 選択状態を解除する
        obj.select_set(False)

    # 指定オブジェクトを選択状態にする
    arg_object.select_set(True)

    # 指定オブジェクトをアクティブにする
    bpy.context.view_layer.objects.active = arg_object

    # レンダリングエンジンを CYCLES に切り替える
    bpy.context.scene.render.engine = 'CYCLES'

    # GPUの利用有無を確認する
    if arg_GPUuse == True:
        # 利用設定ならGPUの設定を行う
        bpy.data.scenes["Scene"].cycles.device = 'GPU'
        # CUDAを選択する
        bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
        # デバイスの一覧を取得する
        for devices in bpy.context.preferences.addons['cycles'].preferences.get_devices():
            for device in devices:
                # デバイスタイプがCUDAならば利用対象とする
                if device.type == 'CUDA':
                    print("利用可能なGPUを検出しました:" + device.name)
                    device.use = True

    # 「粗さ」タイプのベイクを実行する
    # ベイクの種類
    # ('COMBINED', 'AO', 'SHADOW', 'NORMAL', 'UV', 'ROUGHNESS',
    # 'EMIT', 'ENVIRONMENT', 'DIFFUSE', 'GLOSSY', 'TRANSMISSION')
    # (render.bake 以外の設定は引数で指定する必要あり)
    bpy.ops.object.bake(type='ROUGHNESS', margin=arg_bakemargin)

    return


# 対象マテリアルの指定ノードを削除する
def delete_node_target(arg_material:bpy.types.Material, arg_node:bpy.types.Node):
    """対象マテリアルの指定ノードを削除する

    Args:
        arg_material (bpy.types.Material): 対象マテリアル
        arg_node (bpy.types.Node): 指定ノード
    """

    # ノード操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.Node.html)

    # ターゲットマテリアルのノード参照を取得
    mat_nodes = arg_material.node_tree.nodes

    # ノードを削除する
    mat_nodes.remove(arg_node)

    return

