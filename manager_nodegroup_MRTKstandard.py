# bpyインポート
import bpy

# ノードグループ名を定義する
def_nodegroup_name = "MRTKStandardNodeGroup"

# ノードバージョン
def_nodegroup_version = "MRTKStandardNode 1.1"

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
def_rgbmixnode_input_maincolor_name = "Color1"      # メインカラー
def_rgbmixnode_input_subcolor_name = "Color2"       # サブカラー
def_rgbmixnode_output_color_name = "Color"          # カラー出力

# 滑らかさ数値反転ノードで使用する入出力端子の名前を定義する
def_smoothinvnode_input_mainvalue_num = 0           # メイン値入力端子
def_smoothinvnode_input_subvalue_num = 1            # サブ値入力端子
def_smoothinvnode_output_value_name = "Value"       # 値出力


# 指定ノードがMRTKStandardかチェックする
def check_isnode_MRTKStandardNode(arg_node:bpy.types.Node) -> bool:
    """指定ノードがMRTKStandardかチェックする

    Args:
        arg_node (bpy.types.Node): 指定ノード

    Returns:
        bool: MRTKStandardか否か
    """

    # チェック結果
    isMRTKStandard = False

    # ノードタイプを取得する
    node_idname = arg_node.bl_idname

    # ノードタイプがノードグループか確認する
    if node_idname == 'ShaderNodeGroup':
        # ノードグループならツリー情報(ノードグループ)の名前を取得する
        nodetree_name = arg_node.node_tree.name

        # ノードグループのツリー名称が定義と一致するか確認する
        if nodetree_name == def_nodegroup_name:
            # 一致すればMRTKStandardと判定する
            isMRTKStandard = True

    return isMRTKStandard

# 指定ノードがMRTKStandardで透過が0以上かチェックする
def check_trans_MRTKStandardNode(arg_node:bpy.types.Node) -> bool:
    """指定ノードがMRTKStandardで透過が0以上かチェックする

    Args:
        arg_node (bpy.types.Node): 指定ノード

    Returns:
        bool: MRTKStandardで透過が0以上か否か
    """

    # ノードの種類がMRTKStandardチェックする
    isMRTKStandard = check_isnode_MRTKStandardNode(arg_node)

    # MRTKStandardか確認する
    if isMRTKStandard == False:
        # MRTKStandardでない場合はFalseを返す
        return False

    # 透過設定の値を取得する(デフォルトに設定されている値を取得する)
    input_trans = arg_node.inputs[def_inputnode_input_trans_name]
    trans_val = input_trans.default_value

    # チェック結果
    isTrans = False

    # 透過の入力値が0以上か確認する
    if trans_val > 0:
        # 0以上であれば透過設定と判定する
        isTrans = True
        
    return isTrans


# MRTKStandard設定を構成するノードグループを作成する
def new_nodegroup_MRTKStandard() -> bpy.types.NodeGroup:
    """MRTKStandard設定を構成するノードグループを作成する

    Returns:
        bpy.types.NodeGroup: 作成ノードグループの参照
    """

    # データ内に既にMRTKStandardのノードグループが定義されているか確認する
    # (get関数は対象が存在しない場合 None が返る)
    get_nodegroup = bpy.data.node_groups.get(def_nodegroup_name)

    # ノードグループが取得できたか確認する
    if get_nodegroup != None:
        # 既に同名のノードグループが定義されている場合はこれを返す
        return get_nodegroup

    # ノードグループデータを新規作成する
    new_nodegroup = bpy.data.node_groups.new(name=def_nodegroup_name, type='ShaderNodeTree')

    # ノードグループに入力ノードを作成する
    group_inputnode = add_nodegroup_MRTKStandard_inputs()

    # ノードグループに出力ノードを作成する
    group_outputnode = add_nodegroup_MRTKStandard_outputs()

    # ノードグループにBSDFノードを作成する
    group_bsdfnode = add_nodegroup_MRTKStandard_bsdfnode()

    # ノードグループにRGBミックスノードを作成する
    group_rgbmix = add_nodegroup_MRTKStandard_rgbmixnode()

    # ノードグループに滑らかさ数値反転ノードを作成する
    group_smoothinversion = add_nodegroup_MRTKStandard_smoothinversionnode()

    # ノードグループを構成するのリンク情報を設定する
    link_result = link_MRTKStandardNodeGroup_default()

    return new_nodegroup

# マテリアルのノードツリーにMRTKStandardノードグループを追加する
def add_nodegroup_target(arg_material:bpy.types.Material) -> bpy.types.Node:
    """マテリアルのノードツリーにMRTKStandardノードグループを追加する

    Args:
        arg_material (bpy.types.Material): 指定マテリアル

    Returns:
        bpy.types.Node: 作成ノードの参照
    """

    # 新規マテリアルのノードグループ参照を取得する
    mat_nodes = arg_material.node_tree.nodes

    # ノードグループを追加する
    nodegroup_node = mat_nodes.new(type='ShaderNodeGroup')
    nodegroup_node.location = (-100, 0)

    # データの参照をカスタムノードに変更する
    nodegroup_node.node_tree = bpy.data.node_groups[def_nodegroup_name]

    return nodegroup_node

# MRTKStandard設定を構成するノードグループの入力UIを設定する
def setting_node_MRTKStandard_ui(arg_node:bpy.types.Node) -> bpy.types.Node:
    """MRTKStandard設定を構成するノードグループの入力UIを設定する

    Args:
        arg_node (bpy.types.Node): 指定ノードグループ(ノード参照)

    Returns:
        bpy.types.Node: 作成ノードの参照
    """

    # ノードバージョンをラベルに記述する
    arg_node.label = def_nodegroup_version

    # ノーマル設定のデフォルト値を隠蔽する
    input_normal = arg_node.inputs[def_inputnode_input_normal_name]
    input_normal.hide_value = True

    return arg_node


# MRTKStandard設定を構成するノードグループの入力ノードを作成する
def add_nodegroup_MRTKStandard_inputs() -> bpy.types.Node:
    """MRTKStandard設定を構成するノードグループの入力ノードを作成する

    Args:
        arg_nodegroup (bpy.types.NodeGroup): 指定ノードグループ

    Returns:
        bpy.types.Node: 作成ノードの参照
    """

    # データ内に既にMRTKStandardのノードグループが定義されているか確認する
    # (get関数は対象が存在しない場合 None が返る)
    get_nodegroup = bpy.data.node_groups.get(def_nodegroup_name)

    # ノードグループが取得できたか確認する
    if get_nodegroup == None:
        # 既にMRTKStandardのノードグループが定義されていない場合は処理しない
        return None

    # ノードグループの入力情報を作成する
    group_inputs = get_nodegroup.nodes.new(type='NodeGroupInput')
    group_inputs.name = def_inputnode_name

    # 入力ノードの配置座標を設定する
    group_inputs.location = (-800,0)

    # ベースカラーの入力ソケットを設定する
    socket_basecolor = get_nodegroup.inputs.new('NodeSocketColor', def_inputnode_input_color_name)
    socket_basecolor.default_value = (0.8, 0.8, 0.8, 1.0)

    # メタリックの入力ソケットを設定する
    socket_metallic = get_nodegroup.inputs.new('NodeSocketFloatFactor', def_inputnode_input_metallic_name)
    socket_metallic.default_value = 0.0
    socket_metallic.min_value = 0.0
    socket_metallic.max_value = 1.0

    # 滑らかさの入力ソケットを設定する
    socket_smoothness = get_nodegroup.inputs.new('NodeSocketFloatFactor', def_inputnode_input_smoothness_name)
    socket_smoothness.default_value = 0.5
    socket_smoothness.min_value = 0.0
    socket_smoothness.max_value = 1.0

    # 透過切り替えの入力ソケットを設定する
    socket_transmission = get_nodegroup.inputs.new('NodeSocketInt', def_inputnode_input_trans_name)
    socket_transmission.default_value = 0
    socket_transmission.min_value = 0
    socket_transmission.max_value = 1

    # エミッション強度の入力ソケットを設定する
    socket_emission = get_nodegroup.inputs.new('NodeSocketFloatFactor', def_inputnode_input_emission_name)
    socket_emission.default_value = 0.0
    socket_emission.min_value = 0.0
    socket_emission.max_value = 1.0

    # 法線情報の入力ソケットを設定する
    socket_normal = get_nodegroup.inputs.new('NodeSocketVector', def_inputnode_input_normal_name)

    return group_inputs


# MRTKStandard設定を構成するノードグループの出力ノードを作成する
def add_nodegroup_MRTKStandard_outputs() -> bpy.types.Node:
    """MRTKStandard設定を構成するノードグループの出力ノードを作成する

    Args:
        arg_nodegroup (bpy.types.NodeGroup): 指定ノードグループ

    Returns:
        bpy.types.Node: 作成ノードの参照
    """

    # データ内に既にMRTKStandardのノードグループが定義されているか確認する
    # (get関数は対象が存在しない場合 None が返る)
    get_nodegroup = bpy.data.node_groups.get(def_nodegroup_name)

    # ノードグループが取得できたか確認する
    if get_nodegroup == None:
        # 既にMRTKStandardのノードグループが定義されていない場合は処理しない
        return None

    # ノードグループの入力情報を作成する
    group_outputs = get_nodegroup.nodes.new(type='NodeGroupOutput')
    group_outputs.name = def_outputnode_name

    # 入力ノードの配置座標を設定する
    group_outputs.location = (600,0)

    # シェーダーの出力ソケットを設定する
    socket_bsdf = get_nodegroup.outputs.new('NodeSocketShader', def_outputnode_output_shader_name)

    return group_outputs

# MRTKStandard設定を構成するノードグループのBSDFノードを作成する
def add_nodegroup_MRTKStandard_bsdfnode() -> bpy.types.Node:
    """MRTKStandard設定を構成するノードグループのBSDFノードを作成する

    Args:
        arg_nodegroup (bpy.types.NodeGroup): 指定ノードグループ

    Returns:
        bpy.types.Node: 作成ノードの参照
    """

    # データ内に既にMRTKStandardのノードグループが定義されているか確認する
    # (get関数は対象が存在しない場合 None が返る)
    get_nodegroup = bpy.data.node_groups.get(def_nodegroup_name)

    # ノードグループが取得できたか確認する
    if get_nodegroup == None:
        # 既にMRTKStandardのノードグループが定義されていない場合は処理しない
        return None

    # ノードグループにプリンシプルBSDFノードを作成する
    group_bsdf = get_nodegroup.nodes.new(type='ShaderNodeBsdfPrincipled')
    group_bsdf.name = def_bsdfnode_name

    # BSDFノードの配置座標を設定する
    group_bsdf.location = (100,0)

    return group_bsdf

# MRTKStandard設定を構成するノードグループのRGBミックスノードを作成する
def add_nodegroup_MRTKStandard_rgbmixnode() -> bpy.types.Node:
    """MRTKStandard設定を構成するノードグループのRGBミックスノードを作成する

    Args:
        arg_nodegroup (bpy.types.NodeGroup): 指定ノードグループ

    Returns:
        bpy.types.Node: 作成ノードの参照
    """

    # データ内に既にMRTKStandardのノードグループが定義されているか確認する
    # (get関数は対象が存在しない場合 None が返る)
    get_nodegroup = bpy.data.node_groups.get(def_nodegroup_name)

    # ノードグループが取得できたか確認する
    if get_nodegroup == None:
        # 既にMRTKStandardのノードグループが定義されていない場合は処理しない
        return None

    # ノードグループにRGBミックスノードを作成する
    group_rgbmix = get_nodegroup.nodes.new(type='ShaderNodeMixRGB')
    group_rgbmix.name = def_rgbmixnode_name

    # RGBミックスの配置座標を設定する
    group_rgbmix.location = (-300,-400)

    # メインカラーのソケットを設定する(黒色)
    input_color1 = group_rgbmix.inputs[def_rgbmixnode_input_maincolor_name]
    input_color1.default_value = (0.0, 0.0, 0.0, 1.0)

    # サブカラーのソケットを設定する(白色)
    input_color1 = group_rgbmix.inputs[def_rgbmixnode_input_subcolor_name]
    input_color1.default_value = (1.0, 1.0, 1.0, 1.0)

    return group_rgbmix

# MRTKStandard設定を構成するノードグループの滑らかさ数値反転(0.0 <-> 1.0)ノードを作成する
def add_nodegroup_MRTKStandard_smoothinversionnode() -> bpy.types.Node:
    """MRTKStandard設定を構成するノードグループの滑らかさ数値反転(0.0 <-> 1.0)ノードを作成する

    Args:
        arg_nodegroup (bpy.types.NodeGroup): 指定ノードグループ

    Returns:
        bpy.types.Node: 作成ノードの参照
    """

    # データ内に既にMRTKStandardのノードグループが定義されているか確認する
    # (get関数は対象が存在しない場合 None が返る)
    get_nodegroup = bpy.data.node_groups.get(def_nodegroup_name)

    # ノードグループが取得できたか確認する
    if get_nodegroup == None:
        # 既にMRTKStandardのノードグループが定義されていない場合は処理しない
        return None

    # ノードグループに数式ノードを作成する
    group_smoothinversion = get_nodegroup.nodes.new(type='ShaderNodeMath')
    group_smoothinversion.name = def_smoothinvnode_name

    # 数式ノードの配置座標を設定する
    group_smoothinversion.location = (-300,-200)

    # 数式を「減算」に指定する
    group_smoothinversion.operation = 'SUBTRACT'

    # 範囲制限を有効にする
    group_smoothinversion.use_clamp = True

    # メイン入力端子のソケットを設定する(固定値１)
    input_value1 = group_smoothinversion.inputs[def_smoothinvnode_input_mainvalue_num]
    input_value1.default_value = 1.0

    # サブ入力端子のソケットを設定する(入力用)
    input_value1 = group_smoothinversion.inputs[def_smoothinvnode_input_subvalue_num]
    input_value1.default_value = 0.5

    return group_smoothinversion


# MRTKStandard設定を構成するノードグループのノードリンクを作成する
def link_MRTKStandardNodeGroup_default() -> bool:
    """MRTKStandard設定を構成するノードグループのノードリンクを作成する

    Returns:
        bool: 実行正否
    """

    # データ内に既にMRTKStandardのノードグループが定義されているか確認する
    # (get関数は対象が存在しない場合 None が返る)
    mrtkstandard_nodegroup = bpy.data.node_groups.get(def_nodegroup_name)

    # ノードグループが取得できたか確認する
    if mrtkstandard_nodegroup == None:
        # 既にMRTKStandardのノードグループが定義されていない場合は処理しない
        return None

    # ノードリンクを取得する
    mrtkstandard_links = mrtkstandard_nodegroup.links

    # 全てのリンクをクリアする
    mrtkstandard_links.clear()

    # 各種ノードを取得する
    mrtkstandard_inputnode = mrtkstandard_nodegroup.nodes[def_inputnode_name]         # 入力ノード
    mrtkstandard_outputnode = mrtkstandard_nodegroup.nodes[def_outputnode_name]       # 出力ノード
    mrtkstandard_bsdfnode = mrtkstandard_nodegroup.nodes[def_bsdfnode_name]           # プリンシプルBSDFノード
    mrtkstandard_rgbmixnode = mrtkstandard_nodegroup.nodes[def_rgbmixnode_name]       # RGBミックスノード
    mrtkstandard_smoothinvnode = mrtkstandard_nodegroup.nodes[def_smoothinvnode_name] # 滑らかさ数値反転ノード

    # 入力ノードへの接続を行う
    
    # ベースカラー
    # (inputベースカラー -> bsdfベースカラー)
    mrtkstandard_links.new(
        mrtkstandard_inputnode.outputs[def_inputnode_input_color_name],
        mrtkstandard_bsdfnode.inputs[def_bsdfnode_input_color_name]
    )
    # (inputベースカラー -> rgbmixサブカラー)
    mrtkstandard_links.new(
        mrtkstandard_inputnode.outputs[def_inputnode_input_color_name],
        mrtkstandard_rgbmixnode.inputs[def_rgbmixnode_input_subcolor_name]
    )
    
    # メタリック
    # (inputメタリック -> bsdfメタリック)
    mrtkstandard_links.new(
        mrtkstandard_inputnode.outputs[def_inputnode_input_metallic_name],
        mrtkstandard_bsdfnode.inputs[def_bsdfnode_input_metallic_name]
    )
    
    # 滑らかさ
    # (input滑らかさ -> smoothinversionサブ値入力端子)
    mrtkstandard_links.new(
        mrtkstandard_inputnode.outputs[def_inputnode_input_smoothness_name],
        mrtkstandard_smoothinvnode.inputs[def_smoothinvnode_input_subvalue_num]
    )
    
    # 透過
    # (input透過 -> bsdf伝播)
    mrtkstandard_links.new(
        mrtkstandard_inputnode.outputs[def_inputnode_input_trans_name],
        mrtkstandard_bsdfnode.inputs[def_bsdfnode_input_trans_name]
    )
    
    # 放射
    # (input放射 -> rgbmix係数)
    mrtkstandard_links.new(
        mrtkstandard_inputnode.outputs[def_inputnode_input_emission_name],
        mrtkstandard_rgbmixnode.inputs[def_rgbmixnode_input_factor_name]
    )
    
    # ノーマル
    # (inputノーマル -> bsdfノーマル)
    mrtkstandard_links.new(
        mrtkstandard_inputnode.outputs[def_inputnode_input_normal_name],
        mrtkstandard_bsdfnode.inputs[def_bsdfnode_input_normal_name]
    )


    # ノードグループ内の接続を行う

    # 放射
    # (rgbmix出力 -> bsdf放射)
    mrtkstandard_links.new(
        mrtkstandard_rgbmixnode.outputs[def_rgbmixnode_output_color_name],
        mrtkstandard_bsdfnode.inputs[def_bsdfnode_input_emission_name]
    )

    # 粗さ
    # (smoothinversion出力 -> bsdf粗さ)
    mrtkstandard_links.new(
        mrtkstandard_smoothinvnode.outputs[def_smoothinvnode_output_value_name],
        mrtkstandard_bsdfnode.inputs[def_bsdfnode_input_roughness_name]
    )


    # 出力ノードへの接続を行う

    # シェーダ出力
    # (bsdfシェーダ出力 -> outputシェーダ出力)
    mrtkstandard_links.new(
        mrtkstandard_bsdfnode.outputs[def_bsdfnode_output_shader_name],
        mrtkstandard_outputnode.inputs[def_outputnode_output_shader_name]
    )

    return True


# MRTKStandardのシンプルカラーの接続を切り替える
def link_MRTKStandardNodeGroup_switch_simple_color() -> bool:
    """MRTKStandardのシンプルカラーの接続を切り替える

    Returns:
        bool: 実行正否
    """

    # 事前にMRTKStandardのノードグループの接続をリセットする
    link_result = link_MRTKStandardNodeGroup_default()

    # データ内に既にMRTKStandardのノードグループが定義されているか確認する
    # (get関数は対象が存在しない場合 None が返る)
    mrtkstandard_nodegroup = bpy.data.node_groups.get(def_nodegroup_name)

    # ノードグループが取得できたか確認する
    if mrtkstandard_nodegroup == None:
        # 既にMRTKStandardのノードグループが定義されていない場合は処理しない
        return None

    # ノードリンクを取得する
    mrtkstandard_links = mrtkstandard_nodegroup.links

    # 各種ノードを取得する
    mrtkstandard_inputnode = mrtkstandard_nodegroup.nodes[def_inputnode_name]         # 入力ノード
    mrtkstandard_outputnode = mrtkstandard_nodegroup.nodes[def_outputnode_name]       # 出力ノード
    mrtkstandard_bsdfnode = mrtkstandard_nodegroup.nodes[def_bsdfnode_name]           # プリンシプルBSDFノード
    mrtkstandard_rgbmixnode = mrtkstandard_nodegroup.nodes[def_rgbmixnode_name]       # RGBミックスノード
    mrtkstandard_smoothinvnode = mrtkstandard_nodegroup.nodes[def_smoothinvnode_name] # 滑らかさ数値反転ノード

    # BSDFノードのベースカラーに接続された全てのリンクを走査する
    for link in mrtkstandard_bsdfnode.inputs[def_bsdfnode_input_color_name].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)
    
    # BSDFノードのメタリックに接続された全てのリンクを走査する
    for link in mrtkstandard_bsdfnode.inputs[def_bsdfnode_input_metallic_name].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)

    # BSDFノードの粗さに接続された全てのリンクを走査する
    for link in mrtkstandard_bsdfnode.inputs[def_bsdfnode_input_roughness_name].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)
        
    # BSDFノードの伝播に接続された全てのリンクを走査する
    for link in mrtkstandard_bsdfnode.inputs[def_bsdfnode_input_trans_name].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)
        
    # BSDFノードの放射に接続された全てのリンクを走査する
    for link in mrtkstandard_bsdfnode.inputs[def_bsdfnode_input_emission_name].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)
        
    # BSDFノードのノーマルに接続された全てのリンクを走査する
    for link in mrtkstandard_bsdfnode.inputs[def_bsdfnode_input_normal_name].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)

    # ベースカラーのみ再接続する
    # (inputベースカラー -> bsdfベースカラー)
    mrtkstandard_links.new(
        mrtkstandard_inputnode.outputs[def_inputnode_input_color_name],
        mrtkstandard_bsdfnode.inputs[def_bsdfnode_input_color_name]
    )
    
    return True

# 指定ノードのMRTKStandardの滑らかと粗さの反転接続を切り替える
def link_MRTKStandardNodeGroup_inversion_smoothness_roughness() -> bool:
    """指定ノードのMRTKStandardの滑らかと粗さの反転接続を切り替える

    Returns:
        bool: 実行正否
    """

    # 事前にMRTKStandardのノードグループの接続をリセットする
    link_result = link_MRTKStandardNodeGroup_default()

    # データ内に既にMRTKStandardのノードグループが定義されているか確認する
    # (get関数は対象が存在しない場合 None が返る)
    mrtkstandard_nodegroup = bpy.data.node_groups.get(def_nodegroup_name)

    # ノードグループが取得できたか確認する
    if mrtkstandard_nodegroup == None:
        # 既にMRTKStandardのノードグループが定義されていない場合は処理しない
        return None

    # ノードリンクを取得する
    mrtkstandard_links = mrtkstandard_nodegroup.links

    # 各種ノードを取得する
    mrtkstandard_inputnode = mrtkstandard_nodegroup.nodes[def_inputnode_name]         # 入力ノード
    mrtkstandard_outputnode = mrtkstandard_nodegroup.nodes[def_outputnode_name]       # 出力ノード
    mrtkstandard_bsdfnode = mrtkstandard_nodegroup.nodes[def_bsdfnode_name]           # プリンシプルBSDFノード
    mrtkstandard_rgbmixnode = mrtkstandard_nodegroup.nodes[def_rgbmixnode_name]       # RGBミックスノード
    mrtkstandard_smoothinvnode = mrtkstandard_nodegroup.nodes[def_smoothinvnode_name] # 滑らかさ数値反転ノード

    # 入力ノードの滑らかさに接続された全てのリンクを走査する
    for link in mrtkstandard_inputnode.outputs[def_inputnode_input_smoothness_name].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)

    # 滑らかさ数値反転ノードの出力に接続された全てのリンクを走査する
    for link in mrtkstandard_smoothinvnode.outputs[def_smoothinvnode_output_value_name].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)

    # 滑らかさと粗さを反転しないで接続する
    # (input滑らかさ -> smoothinversion端子２)
    mrtkstandard_links.new(
        mrtkstandard_inputnode.outputs[def_inputnode_input_smoothness_name],
        mrtkstandard_bsdfnode.inputs[def_bsdfnode_input_roughness_name]
    )
        
    return True

# 指定ノードのMRTKStandardのメタリックと粗さの接続を切り替える
def link_MRTKStandardNodeGroup_cross_metallic_roughness() -> bool:
    """指定ノードのMRTKStandardのメタリックと粗さの接続を切り替える

    Returns:
        bool: 実行正否
    """

    # 事前にMRTKStandardのノードグループの接続をリセットする
    link_result = link_MRTKStandardNodeGroup_default()

    # データ内に既にMRTKStandardのノードグループが定義されているか確認する
    # (get関数は対象が存在しない場合 None が返る)
    mrtkstandard_nodegroup = bpy.data.node_groups.get(def_nodegroup_name)

    # ノードグループが取得できたか確認する
    if mrtkstandard_nodegroup == None:
        # 既にMRTKStandardのノードグループが定義されていない場合は処理しない
        return None

    # ノードリンクを取得する
    mrtkstandard_links = mrtkstandard_nodegroup.links

    # 各種ノードを取得する
    mrtkstandard_inputnode = mrtkstandard_nodegroup.nodes[def_inputnode_name]         # 入力ノード
    mrtkstandard_outputnode = mrtkstandard_nodegroup.nodes[def_outputnode_name]       # 出力ノード
    mrtkstandard_bsdfnode = mrtkstandard_nodegroup.nodes[def_bsdfnode_name]           # プリンシプルBSDFノード
    mrtkstandard_rgbmixnode = mrtkstandard_nodegroup.nodes[def_rgbmixnode_name]       # RGBミックスノード
    mrtkstandard_smoothinvnode = mrtkstandard_nodegroup.nodes[def_smoothinvnode_name] # 滑らかさ数値反転ノード

    # 入力ノードのメタリックに接続された全てのリンクを走査する
    for link in mrtkstandard_inputnode.outputs[def_inputnode_input_metallic_name].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)

    # 入力ノードの粗さに接続された全てのリンクを走査する
    for link in mrtkstandard_inputnode.outputs[def_inputnode_input_smoothness_name].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)

    # メタリックと粗さを交差して接続する
    # (inputメタリック -> bsdf粗さ)
    mrtkstandard_links.new(
        mrtkstandard_inputnode.outputs[def_inputnode_input_metallic_name],
        mrtkstandard_bsdfnode.inputs[def_bsdfnode_input_roughness_name]
    )
        
    # (input滑らかさ -> smoothinversionサブ値入力端子)
    mrtkstandard_links.new(
        mrtkstandard_inputnode.outputs[def_inputnode_input_smoothness_name],
        mrtkstandard_smoothinvnode.inputs[def_smoothinvnode_input_subvalue_num]
    )

    # (smoothinversion出力 -> bsdfメタリック)
    mrtkstandard_links.new(
        mrtkstandard_smoothinvnode.outputs[def_smoothinvnode_output_value_name],
        mrtkstandard_bsdfnode.inputs[def_bsdfnode_input_metallic_name]
    )
    
    return True

# 指定ノードのMRTKStandardのカラーとRGBミックスの接続有無を切り替える
def link_MRTKStandardNodeGroup_joint_color_rgbmix() -> bool:
    """指定ノードのMRTKStandardのカラーとRGBミックスの接続有無を切り替える

    Returns:
        bool: 実行正否
    """

    # 事前にMRTKStandardのノードグループの接続をリセットする
    link_result = link_MRTKStandardNodeGroup_default()

    # データ内に既にMRTKStandardのノードグループが定義されているか確認する
    # (get関数は対象が存在しない場合 None が返る)
    mrtkstandard_nodegroup = bpy.data.node_groups.get(def_nodegroup_name)

    # ノードグループが取得できたか確認する
    if mrtkstandard_nodegroup == None:
        # 既にMRTKStandardのノードグループが定義されていない場合は処理しない
        return None

    # ノードリンクを取得する
    mrtkstandard_links = mrtkstandard_nodegroup.links

    # 各種ノードを取得する
    mrtkstandard_inputnode = mrtkstandard_nodegroup.nodes[def_inputnode_name]         # 入力ノード
    mrtkstandard_outputnode = mrtkstandard_nodegroup.nodes[def_outputnode_name]       # 出力ノード
    mrtkstandard_bsdfnode = mrtkstandard_nodegroup.nodes[def_bsdfnode_name]           # プリンシプルBSDFノード
    mrtkstandard_rgbmixnode = mrtkstandard_nodegroup.nodes[def_rgbmixnode_name]       # RGBミックスノード
    mrtkstandard_smoothinvnode = mrtkstandard_nodegroup.nodes[def_smoothinvnode_name] # 滑らかさ数値反転ノード

    # 入力ノードのベースカラーに接続された全てのリンクを走査する
    for link in mrtkstandard_inputnode.outputs[def_inputnode_input_color_name].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)

    # RGBノードのベースカラーのみ再接続する
    # (inputベースカラー -> bsdfベースカラー)
    mrtkstandard_links.new(
        mrtkstandard_inputnode.outputs[def_inputnode_input_color_name],
        mrtkstandard_bsdfnode.inputs[def_bsdfnode_input_color_name]
    )

    return True



