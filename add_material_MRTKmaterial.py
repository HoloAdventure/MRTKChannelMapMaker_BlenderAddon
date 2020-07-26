# bpyインポート
import bpy

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

    # MRTKStandard設定のノードグループを作成する
    make_nodegroup = new_nodegroup_MRTKStandard()

    # マテリアルのノードツリーに指定のノードグループを追加する
    make_shadenode = add_nodegroup_target(arg_material=make_mat, arg_nodegroup=make_nodegroup)

    # MRTKStandard設定のノードグループの入力UIを調整する
    make_shadenode = setting_nodegroup_MRTKStandard_ui(arg_node=make_shadenode)

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

# マテリアルのノードツリーにノードグループを追加する
def add_nodegroup_target(arg_material:bpy.types.Material, arg_nodegroup:bpy.types.NodeGroup) -> bpy.types.Node:
    """マテリアルのノードツリーにノードグループを追加する

    Args:
        arg_material (bpy.types.Material): 指定マテリアル
        arg_nodegroup (bpy.types.NodeGroup): 指定ノードグループ

    Returns:
        bpy.types.Node: 作成ノードの参照
    """

    # 新規マテリアルのノードグループ参照を取得する
    mat_nodes = arg_material.node_tree.nodes

    # ノードグループを追加する
    nodegroup_node = mat_nodes.new(type='ShaderNodeGroup')
    nodegroup_node.location = (-100, 0)

    # データの参照をカスタムノードに変更する
    nodegroup_node.node_tree = bpy.data.node_groups[arg_nodegroup.name]

    return nodegroup_node

# MRTKStandard設定を構成するノードグループを作成する
def new_nodegroup_MRTKStandard() -> bpy.types.NodeGroup:
    """MRTKStandard設定を構成するノードグループを作成する

    Returns:
        bpy.types.NodeGroup: 作成ノードグループの参照
    """

    # ノードグループ名を定義する
    nodegroup_name = "MRTKStandardNodeGroup"

    # データ内に既に同名のノードグループが定義されているか確認する
    # (get関数は対象が存在しない場合 None が返る)
    get_nodegroup = bpy.data.node_groups.get(nodegroup_name)

    # ノードグループが取得できたか確認する
    if get_nodegroup != None:
        # 既に同名のノードグループが定義されている場合はこれを返す
        return get_nodegroup

    # ノードグループデータを新規作成する
    new_nodegroup = bpy.data.node_groups.new(name=nodegroup_name, type='ShaderNodeTree')

    # ノードグループに入力ノードを作成する
    group_inputnode = add_nodegroup_MRTKStandard_inputs(arg_nodegroup=new_nodegroup)

    # ノードグループに出力ノードを作成する
    group_outputnode = add_nodegroup_MRTKStandard_outputs(arg_nodegroup=new_nodegroup)

    # ノードグループにBSDFノードを作成する
    group_bsdfnode = add_nodegroup_MRTKStandard_bsdfnode(arg_nodegroup=new_nodegroup)

    # ノードグループにRGBミックスノードを作成する
    group_rgbmix = add_nodegroup_MRTKStandard_rgbmixnode(arg_nodegroup=new_nodegroup)

    # ノードグループに滑らかさ数値反転ノードを作成する
    group_smoothinversion = add_nodegroup_MRTKStandard_smoothinversionnode(arg_nodegroup=new_nodegroup)

    # ノードグループを構成するのリンク情報を設定する
    group_links = add_nodegroup_MRTKStandard_links(
        arg_nodegroup=new_nodegroup,
        arg_inputnode=group_inputnode,
        arg_outputnode=group_outputnode,
        arg_bsdfnode=group_bsdfnode,
        arg_rgbmix=group_rgbmix,
        arg_smoothinversion=group_smoothinversion
    )

    return new_nodegroup

# MRTKStandard設定を構成するノードグループの入力ノードを作成する
def add_nodegroup_MRTKStandard_inputs(arg_nodegroup:bpy.types.NodeGroup) -> bpy.types.Node:
    """MRTKStandard設定を構成するノードグループの入力ノードを作成する

    Args:
        arg_nodegroup (bpy.types.NodeGroup): 指定ノードグループ

    Returns:
        bpy.types.Node: 作成ノードの参照
    """

    # 入力ノード名を定義する
    inputnode_name = "MRTKStandardInputNode"

    # ノードグループの入力情報を作成する
    group_inputs = arg_nodegroup.nodes.new(type='NodeGroupInput')
    group_inputs.name = inputnode_name

    # 入力ノードの配置座標を設定する
    group_inputs.location = (-800,0)

    # ベースカラーの入力ソケットを設定する
    socket_basecolor = arg_nodegroup.inputs.new('NodeSocketColor','Base Color')
    socket_basecolor.default_value = (0.8, 0.8, 0.8, 1.0)

    # メタリックの入力ソケットを設定する
    socket_metallic = arg_nodegroup.inputs.new('NodeSocketFloatFactor','Metallic')
    socket_metallic.default_value = 0.0
    socket_metallic.min_value = 0.0
    socket_metallic.max_value = 1.0

    # 滑らかさの入力ソケットを設定する
    socket_smoothness = arg_nodegroup.inputs.new('NodeSocketFloatFactor','Smoothness')
    socket_smoothness.default_value = 0.5
    socket_smoothness.min_value = 0.0
    socket_smoothness.max_value = 1.0

    # 透過切り替えの入力ソケットを設定する
    socket_transmission = arg_nodegroup.inputs.new('NodeSocketInt','Transmission')
    socket_transmission.default_value = 0
    socket_transmission.min_value = 0
    socket_transmission.max_value = 1

    # エミッション強度の入力ソケットを設定する
    socket_emission = arg_nodegroup.inputs.new('NodeSocketFloatFactor','Emission')
    socket_emission.default_value = 0.0
    socket_emission.min_value = 0.0
    socket_emission.max_value = 1.0

    # 法線情報の入力ソケットを設定する
    socket_normal = arg_nodegroup.inputs.new('NodeSocketVector','Normal')

    return group_inputs


# MRTKStandard設定を構成するノードグループの出力ノードを作成する
def add_nodegroup_MRTKStandard_outputs(arg_nodegroup:bpy.types.NodeGroup) -> bpy.types.Node:
    """MRTKStandard設定を構成するノードグループの出力ノードを作成する

    Args:
        arg_nodegroup (bpy.types.NodeGroup): 指定ノードグループ

    Returns:
        bpy.types.Node: 作成ノードの参照
    """

    # 出力ノード名を定義する
    outputnode_name = "MRTKStandardOutputNode"

    # ノードグループの入力情報を作成する
    group_outputs = arg_nodegroup.nodes.new(type='NodeGroupOutput')
    group_outputs.name = outputnode_name

    # 入力ノードの配置座標を設定する
    group_outputs.location = (600,0)

    # シェーダーの出力ソケットを設定する
    socket_bsdf = arg_nodegroup.outputs.new('NodeSocketShader','BSDF')

    return group_outputs

# MRTKStandard設定を構成するノードグループのBSDFノードを作成する
def add_nodegroup_MRTKStandard_bsdfnode(arg_nodegroup:bpy.types.NodeGroup) -> bpy.types.Node:
    """MRTKStandard設定を構成するノードグループのBSDFノードを作成する

    Args:
        arg_nodegroup (bpy.types.NodeGroup): 指定ノードグループ

    Returns:
        bpy.types.Node: 作成ノードの参照
    """

    # プリンシプルBSDFノード名を定義する
    bsdfnode_name = "MRTKStandardBSDFNode"

    # ノードグループにプリンシプルBSDFノードを作成する
    group_bsdf = arg_nodegroup.nodes.new(type='ShaderNodeBsdfPrincipled')
    group_bsdf.name = bsdfnode_name

    # BSDFノードの配置座標を設定する
    group_bsdf.location = (100,0)

    return group_bsdf

# MRTKStandard設定を構成するノードグループのRGBミックスノードを作成する
def add_nodegroup_MRTKStandard_rgbmixnode(arg_nodegroup:bpy.types.NodeGroup) -> bpy.types.Node:
    """MRTKStandard設定を構成するノードグループのRGBミックスノードを作成する

    Args:
        arg_nodegroup (bpy.types.NodeGroup): 指定ノードグループ

    Returns:
        bpy.types.Node: 作成ノードの参照
    """

    # RGBミックスノード名を定義する
    rgbmixnode_name = "MRTKStandardRGBMix"

    # ノードグループにRGBミックスノードを作成する
    group_rgbmix = arg_nodegroup.nodes.new(type='ShaderNodeMixRGB')
    group_rgbmix.name = rgbmixnode_name

    # RGBミックスの配置座標を設定する
    group_rgbmix.location = (-300,-400)

    # カラー１のソケットを設定する(黒色)
    input_color1 = group_rgbmix.inputs['Color1']
    input_color1.default_value = (0.0, 0.0, 0.0, 1.0)

    # カラー２のソケットを設定する(白色)
    input_color1 = group_rgbmix.inputs['Color2']
    input_color1.default_value = (1.0, 1.0, 1.0, 1.0)

    return group_rgbmix

# MRTKStandard設定を構成するノードグループの滑らかさ数値反転(0.0 <-> 1.0)ノードを作成する
def add_nodegroup_MRTKStandard_smoothinversionnode(arg_nodegroup:bpy.types.NodeGroup) -> bpy.types.Node:
    """MRTKStandard設定を構成するノードグループの滑らかさ数値反転(0.0 <-> 1.0)ノードを作成する

    Args:
        arg_nodegroup (bpy.types.NodeGroup): 指定ノードグループ

    Returns:
        bpy.types.Node: 作成ノードの参照
    """

    # 滑らかさ数値反転ノード名を定義する
    smoothinversionnode_name = "MRTKStandardSmoothInversion"

    # ノードグループに数式ノードを作成する
    group_smoothinversion = arg_nodegroup.nodes.new(type='ShaderNodeMath')
    group_smoothinversion.name = smoothinversionnode_name

    # 数式ノードの配置座標を設定する
    group_smoothinversion.location = (-300,-200)

    # 数式を「減算」に指定する
    group_smoothinversion.operation = 'SUBTRACT'

    # 範囲制限を有効にする
    group_smoothinversion.use_clamp = True

    # 入力端子１のソケットを設定する(固定値１)
    input_value1 = group_smoothinversion.inputs[0]
    input_value1.default_value = 1.0

    # 入力端子２のソケットを設定する(入力用)
    input_value1 = group_smoothinversion.inputs[1]
    input_value1.default_value = 0.5

    return group_smoothinversion

# MRTKStandard設定を構成するノードグループの入力UIを調整する
def setting_nodegroup_MRTKStandard_ui(arg_node:bpy.types.Node) -> bpy.types.Node:
    """MRTKStandard設定を構成するノードグループの入力UIを調整する

    Args:
        arg_node (bpy.types.Node): 指定ノードグループ(ノード参照)

    Returns:
        bpy.types.Node: 作成ノードの参照
    """

    # ノーマル設定のデフォルト値を隠蔽する
    input_normal = arg_node.inputs['Normal']
    input_normal.hide_value = True

    return arg_node

# MRTKStandard設定を構成するノードグループのノードリンクを作成する
def add_nodegroup_MRTKStandard_links(arg_nodegroup:bpy.types.NodeGroup, 
  arg_inputnode:bpy.types.Node, arg_outputnode:bpy.types.Node,
  arg_bsdfnode:bpy.types.Node, arg_rgbmix:bpy.types.Node,
  arg_smoothinversion:bpy.types.Node) -> bpy.types.NodeLinks:
    """MRTKStandard設定を構成するノードグループのノードリンクを作成する

    Args:
        arg_nodegroup (bpy.types.NodeGroup): 指定ノードグループ
        arg_inputnode (bpy.types.Node): 入力ノード
        arg_outputnode (bpy.types.Node): 出力ノード
        arg_bsdfnode (bpy.types.Node): BSDFノード
        arg_rgbmix (bpy.types.Node): RGBミックスノード

    Returns:
        bpy.types.NodeLinks: 作成ノードリンクの参照
    """

    # ノードリンクを取得する
    nodegroup_links = arg_nodegroup.links

    # 入力ノードへの接続を行う
    
    # ベースカラー
    # (inputベースカラー -> bsdfベースカラー)
    nodegroup_links.new(arg_inputnode.outputs['Base Color'], arg_bsdfnode.inputs['Base Color'])
    # (inputベースカラー -> rgbmixカラー2)
    nodegroup_links.new(arg_inputnode.outputs['Base Color'], arg_rgbmix.inputs['Color2'])
    
    # メタリック
    # (inputメタリック -> bsdfメタリック)
    nodegroup_links.new(arg_inputnode.outputs['Metallic'], arg_bsdfnode.inputs['Metallic'])
    
    # 滑らかさ
    # (input滑らかさ -> smoothinversion端子２)
    nodegroup_links.new(arg_inputnode.outputs['Smoothness'], arg_smoothinversion.inputs[1])
    
    # 透過
    # (input透過 -> bsdf伝播)
    nodegroup_links.new(arg_inputnode.outputs['Transmission'], arg_bsdfnode.inputs['Transmission'])
    
    # 放射
    # (input放射 -> rgbmix係数)
    nodegroup_links.new(arg_inputnode.outputs['Emission'], arg_rgbmix.inputs['Fac'])
    
    # ノーマル
    # (inputノーマル -> bsdfノーマル)
    nodegroup_links.new(arg_inputnode.outputs['Normal'], arg_bsdfnode.inputs['Normal'])


    # ノードグループ内の接続を行う

    # 放射
    # (rgbmix出力 -> bsdf放射)
    nodegroup_links.new(arg_rgbmix.outputs['Color'], arg_bsdfnode.inputs['Emission'])

    # 粗さ
    # (smoothinversion出力 -> bsdf粗さ)
    nodegroup_links.new(arg_smoothinversion.outputs['Value'], arg_bsdfnode.inputs['Roughness'])


    # 出力ノードへの接続を行う

    # シェーダ出力
    # (bsdfシェーダ出力 -> outputシェーダ出力)
    nodegroup_links.new(arg_bsdfnode.outputs['BSDF'], arg_outputnode.inputs['BSDF'])

    return nodegroup_links


