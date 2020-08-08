# 各種ライブラリインポート
if "bpy" in locals():
    import importlib
    if "accessor_control_MRTKstandard" in locals():
        importlib.reload(accessor_control_MRTKstandard)
import bpy
from . import accessor_control_MRTKstandard

# 指定オブジェクトにノードグループの新規マテリアルを参照するマテリアルスロットを作成する
def add_materialslot_nodegroupmaterial(arg_object:bpy.types.Object, arg_materialname="DefaultMaterial") -> bool:
    """指定オブジェクトにノードグループの新規マテリアルを参照するマテリアルスロットを作成する

    Args:
        arg_object (bpy.types.Object): 指定オブジェクト
        arg_materialname (str, optional): 作成マテリアル名. Defaults to "DefaultMaterial".

    Returns:
        bool: 実行正否
    """

    # 空のノードの新規マテリアルを作成する
    make_mat = new_material_emptynode(arg_materialname=arg_materialname)

    # 作成したマテリアルをオブジェクトのマテリアルスロットに追加する
    make_matslot = add_materialslot_target(arg_object=arg_object, arg_material=make_mat)

    # マテリアルのノードツリーに出力ノードを追加する
    make_outputnode = add_outputnode_simple(arg_material=make_mat)

    # 指定マテリアルにMRTKStandardノードグループを追加する
    make_shadenode = accessor_control_MRTKstandard.add_nodegroup_MRTKstandard(arg_material=make_mat)

    # 指定マテリアルのノード入出力をリンクする
    link_node_target(arg_material=make_mat, arg_output=make_shadenode.outputs[0], arg_input=make_outputnode.inputs[0])

    return True

# 空ノードの新規マテリアルを作成する
def new_material_emptynode(arg_materialname:str="EmptyNodeMaterial") -> bpy.types.Material:
    """空ノードの新規マテリアルを作成する

    Args:
        arg_materialname (str, optional): 作成マテリアル名. Defaults to "EmptyNodeMaterial".

    Returns:
        bpy.types.Material: 作成マテリアルの参照
    """

    # 新規マテリアルを作成する
    newmaterial = bpy.data.materials.new(arg_materialname)

    # ノードを使用する
    newmaterial.use_nodes = True

    # 新規マテリアルのノード参照を取得する
    mat_nodes = newmaterial.node_tree.nodes

    # マテリアル内の全ノードを走査する
    for delete_node in mat_nodes:
        # ノードを削除する
        mat_nodes.remove(delete_node)

    return newmaterial

# 指定オブジェクトのマテリアルスロットに指定マテリアルを追加する
def add_materialslot_target(arg_object:bpy.types.Object, arg_material:bpy.types.Material) -> bpy.types.MaterialSlot:
    """指定オブジェクトのマテリアルスロットに指定マテリアルを追加する

    Args:
        arg_object (bpy.types.Object): 指定オブジェクト
        arg_material (bpy.types.Material): 指定マテリアル

    Returns:
        bpy.types.MaterialSlot: 作成マテリアルスロットの参照
    """

    # 指定オブジェクトがメッシュオブジェクトか確認する
    if arg_object.type != 'MESH':
        # メッシュオブジェクトでない場合は処理しない
        return False
    
    # メッシュデータの参照を取得する
    mesh = arg_object.data

    # メッシュのマテリアルを追加する
    mesh.materials.append(arg_material)

    # 追加したマテリアルスロットを取得する
    add_matslot = arg_object.material_slots[-1]

    return add_matslot

# 指定マテリアルのノード入出力をリンクする
def link_node_target(arg_material:bpy.types.Material,
  arg_output:bpy.types.NodeSocket, arg_input:bpy.types.NodeSocket) -> bpy.types.NodeLink:
    """指定マテリアルのノード入出力をリンクする

    Args:
        arg_material (bpy.types.Material): 指定マテリアル
        arg_output (bpy.types.NodeSocket): 接続出力ソケット
        arg_input (bpy.types.NodeSocket): 接続入力ソケット

    Returns:
        bpy.types.NodeLink: ノードリンクの参照
    """

    # ターゲットマテリアルのノードリンク参照を取得する
    mat_links = arg_material.node_tree.links

    # 指定ノードの入出力を接続する
    mat_link = mat_links.new(arg_output, arg_input)

    return mat_link

# マテリアルのノードツリーに出力ノードを追加する
def add_outputnode_simple(arg_material:bpy.types.Material) -> bpy.types.Node:
    """マテリアルのノードツリーに出力ノードを追加する

    Args:
        arg_material (bpy.types.Material): 指定マテリアル

    Returns:
        bpy.types.Node: 作成ノードの参照
    """

    # 新規マテリアルのノード参照を取得する
    mat_nodes = arg_material.node_tree.nodes

    # 出力ノードを追加する
    output_node = mat_nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (100, 0)

    return output_node


