# bpyインポート
import bpy

# ノードグループ名を定義する
def_nodegroup_name = "MRTKStandardNodeGroup"

# ノードグループ内の各種ノード名を定義する
def_inputnode_name = "MRTKStandardInputNode"           # 入力ノード名
def_outputnode_name = "MRTKStandardOutputNode"         # 出力ノード名
def_bsdfnode_name = "MRTKStandardBSDFNode"             # プリンシプルBSDFノード名
def_rgbmixnode_name = "MRTKStandardRGBMix"             # RGBミックスノード名
def_smoothinvnode_name = "MRTKStandardSmoothInversion" # 滑らかさ数値反転ノード名

# 各種入出力端子の名前を定義する
# 入力ノードの入出力端子の名前を定義する
def_inputnode_input_color_name = "Base Color"       # ベースカラー
def_inputnode_input_metallic_name = "Metallic"      # メタリック
def_inputnode_input_smoothness_name = "Smoothness"  # 滑らかさ
def_inputnode_input_trans_name = "Transmission"     # 透明度
def_inputnode_input_emission_name = "Emission"      # 発光
def_inputnode_input_normal_name = "Normal"          # 法線

# 出力ノードの入出力端子の名前を定義する
def_outputnode_output_shader_name = "BSDF"          # シェーダー出力

# プリンシプルBSDFノードで使用する入出力端子の名前を定義する
def_bsdfnode_input_color_name = "Base Color"        # ベースカラー
def_bsdfnode_input_metallic_name = "Metallic"       # メタリック
def_bsdfnode_input_roughness_name = "Roughness"     # 粗さ
def_bsdfnode_input_trans_name = "Transmission"      # 伝播
def_bsdfnode_input_emission_name = "Emission"       # 発光
def_bsdfnode_input_normal_name = "Normal"           # 法線
def_bsdfnode_output_shader_name = "BSDF"            # シェーダー出力

# RGBミックスノードで使用する入出力端子の名前を定義する
def_rgbmixnode_input_factor_name = "Fac"            # 係数
def_rgbmixnode_input_color01_name = "Color1"        # カラー01
def_rgbmixnode_input_color02_name = "Color2"        # カラー02
def_rgbmixnode_output_color_name = "Color"          # カラー出力

# 滑らかさ数値反転ノードで使用する入出力端子の名前を定義する
def_smoothinvnode_input_value01_num = 0             # 値入力端子01
def_smoothinvnode_input_value02_num = 1             # 値入力端子02
def_smoothinvnode_output_value_name = "Value"       # 値出力


# MRTKStandard設定を構成するノードグループを作成する
def new_nodegroup_MRTKStandard() -> bpy.types.NodeGroup:
    """MRTKStandard設定を構成するノードグループを作成する

    Returns:
        bpy.types.NodeGroup: 作成ノードグループの参照
    """

    # データ内に既に同名のノードグループが定義されているか確認する
    # (get関数は対象が存在しない場合 None が返る)
    get_nodegroup = bpy.data.node_groups.get(def_nodegroup_name)

    # ノードグループが取得できたか確認する
    if get_nodegroup != None:
        # 既に同名のノードグループが定義されている場合はこれを返す
        return get_nodegroup

    # ノードグループデータを新規作成する
    new_nodegroup = bpy.data.node_groups.new(name=def_nodegroup_name, type='ShaderNodeTree')

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

    # ノードグループの入力情報を作成する
    group_inputs = arg_nodegroup.nodes.new(type='NodeGroupInput')
    group_inputs.name = def_inputnode_name

    # 入力ノードの配置座標を設定する
    group_inputs.location = (-800,0)

    # ベースカラーの入力ソケットを設定する
    socket_basecolor = arg_nodegroup.inputs.new('NodeSocketColor', def_inputnode_input_color_name)
    socket_basecolor.default_value = (0.8, 0.8, 0.8, 1.0)

    # メタリックの入力ソケットを設定する
    socket_metallic = arg_nodegroup.inputs.new('NodeSocketFloatFactor', def_inputnode_input_metallic_name)
    socket_metallic.default_value = 0.0
    socket_metallic.min_value = 0.0
    socket_metallic.max_value = 1.0

    # 滑らかさの入力ソケットを設定する
    socket_smoothness = arg_nodegroup.inputs.new('NodeSocketFloatFactor', def_inputnode_input_smoothness_name)
    socket_smoothness.default_value = 0.5
    socket_smoothness.min_value = 0.0
    socket_smoothness.max_value = 1.0

    # 透過切り替えの入力ソケットを設定する
    socket_transmission = arg_nodegroup.inputs.new('NodeSocketInt', def_inputnode_input_trans_name)
    socket_transmission.default_value = 0
    socket_transmission.min_value = 0
    socket_transmission.max_value = 1

    # エミッション強度の入力ソケットを設定する
    socket_emission = arg_nodegroup.inputs.new('NodeSocketFloatFactor', def_inputnode_input_emission_name)
    socket_emission.default_value = 0.0
    socket_emission.min_value = 0.0
    socket_emission.max_value = 1.0

    # 法線情報の入力ソケットを設定する
    socket_normal = arg_nodegroup.inputs.new('NodeSocketVector', def_inputnode_input_normal_name)

    return group_inputs


# MRTKStandard設定を構成するノードグループの出力ノードを作成する
def add_nodegroup_MRTKStandard_outputs(arg_nodegroup:bpy.types.NodeGroup) -> bpy.types.Node:
    """MRTKStandard設定を構成するノードグループの出力ノードを作成する

    Args:
        arg_nodegroup (bpy.types.NodeGroup): 指定ノードグループ

    Returns:
        bpy.types.Node: 作成ノードの参照
    """

    # ノードグループの入力情報を作成する
    group_outputs = arg_nodegroup.nodes.new(type='NodeGroupOutput')
    group_outputs.name = def_outputnode_name

    # 入力ノードの配置座標を設定する
    group_outputs.location = (600,0)

    # シェーダーの出力ソケットを設定する
    socket_bsdf = arg_nodegroup.outputs.new('NodeSocketShader', def_outputnode_output_shader_name)

    return group_outputs

# MRTKStandard設定を構成するノードグループのBSDFノードを作成する
def add_nodegroup_MRTKStandard_bsdfnode(arg_nodegroup:bpy.types.NodeGroup) -> bpy.types.Node:
    """MRTKStandard設定を構成するノードグループのBSDFノードを作成する

    Args:
        arg_nodegroup (bpy.types.NodeGroup): 指定ノードグループ

    Returns:
        bpy.types.Node: 作成ノードの参照
    """

    # ノードグループにプリンシプルBSDFノードを作成する
    group_bsdf = arg_nodegroup.nodes.new(type='ShaderNodeBsdfPrincipled')
    group_bsdf.name = def_bsdfnode_name

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

    # ノードグループにRGBミックスノードを作成する
    group_rgbmix = arg_nodegroup.nodes.new(type='ShaderNodeMixRGB')
    group_rgbmix.name = def_rgbmixnode_name

    # RGBミックスの配置座標を設定する
    group_rgbmix.location = (-300,-400)

    # カラー１のソケットを設定する(黒色)
    input_color1 = group_rgbmix.inputs[def_rgbmixnode_input_color01_name]
    input_color1.default_value = (0.0, 0.0, 0.0, 1.0)

    # カラー２のソケットを設定する(白色)
    input_color1 = group_rgbmix.inputs[def_rgbmixnode_input_color02_name]
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
    group_smoothinversion.name = def_smoothinvnode_name

    # 数式ノードの配置座標を設定する
    group_smoothinversion.location = (-300,-200)

    # 数式を「減算」に指定する
    group_smoothinversion.operation = 'SUBTRACT'

    # 範囲制限を有効にする
    group_smoothinversion.use_clamp = True

    # 入力端子１のソケットを設定する(固定値１)
    input_value1 = group_smoothinversion.inputs[def_smoothinvnode_input_value01_num]
    input_value1.default_value = 1.0

    # 入力端子２のソケットを設定する(入力用)
    input_value1 = group_smoothinversion.inputs[def_smoothinvnode_input_value02_num]
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
    input_normal = arg_node.inputs[def_inputnode_input_normal_name]
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
    nodegroup_links.new(arg_inputnode.outputs[def_inputnode_input_color_name], arg_bsdfnode.inputs[def_bsdfnode_input_color_name])
    # (inputベースカラー -> rgbmixカラー2)
    nodegroup_links.new(arg_inputnode.outputs[def_inputnode_input_color_name], arg_rgbmix.inputs[def_rgbmixnode_input_color02_name])
    
    # メタリック
    # (inputメタリック -> bsdfメタリック)
    nodegroup_links.new(arg_inputnode.outputs[def_inputnode_input_metallic_name], arg_bsdfnode.inputs[def_bsdfnode_input_metallic_name])
    
    # 滑らかさ
    # (input滑らかさ -> smoothinversion端子２)
    nodegroup_links.new(arg_inputnode.outputs[def_inputnode_input_smoothness_name], arg_smoothinversion.inputs[def_smoothinvnode_input_value02_num])
    
    # 透過
    # (input透過 -> bsdf伝播)
    nodegroup_links.new(arg_inputnode.outputs[def_inputnode_input_trans_name], arg_bsdfnode.inputs[def_bsdfnode_input_trans_name])
    
    # 放射
    # (input放射 -> rgbmix係数)
    nodegroup_links.new(arg_inputnode.outputs[def_inputnode_input_emission_name], arg_rgbmix.inputs[def_rgbmixnode_input_factor_name])
    
    # ノーマル
    # (inputノーマル -> bsdfノーマル)
    nodegroup_links.new(arg_inputnode.outputs[def_inputnode_input_normal_name], arg_bsdfnode.inputs[def_bsdfnode_input_normal_name])


    # ノードグループ内の接続を行う

    # 放射
    # (rgbmix出力 -> bsdf放射)
    nodegroup_links.new(arg_rgbmix.outputs[def_rgbmixnode_output_color_name], arg_bsdfnode.inputs[def_bsdfnode_input_emission_name])

    # 粗さ
    # (smoothinversion出力 -> bsdf粗さ)
    nodegroup_links.new(arg_smoothinversion.outputs[def_smoothinvnode_output_value_name], arg_bsdfnode.inputs[def_bsdfnode_input_roughness_name])


    # 出力ノードへの接続を行う

    # シェーダ出力
    # (bsdfシェーダ出力 -> outputシェーダ出力)
    nodegroup_links.new(arg_bsdfnode.outputs[def_bsdfnode_output_shader_name], arg_outputnode.inputs[def_outputnode_output_shader_name])

    return nodegroup_links


