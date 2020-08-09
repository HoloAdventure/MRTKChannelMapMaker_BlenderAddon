# 各種ライブラリインポート
if "bpy" in locals():
    import importlib
    if "manager_nodegroup_MRTKstandard" in locals():
        importlib.reload(manager_nodegroup_MRTKstandard)
import bpy
from . import manager_nodegroup_MRTKstandard

# 指定マテリアルにMRTKStandardノードグループを追加する
def add_nodegroup_MRTKstandard(arg_material:bpy.types.Material) -> bpy.types.Node:
    """指定マテリアルにMRTKStandardノードグループを追加する

    Args:
        arg_material (bpy.types.Material): 指定マテリアル

    Returns:
        bpy.types.Node: 作成ノードの参照
    """
    
    # MRTKStandard設定のノードグループを作成する
    make_nodegroup = manager_nodegroup_MRTKstandard.make_nodegroup_MRTKStandard()

    # マテリアルのノードツリーに指定のノードグループを追加する
    make_shadenode = manager_nodegroup_MRTKstandard.add_nodegroup_target(arg_material=arg_material)

    # MRTKStandard設定のノードグループの入力UIを設定する
    make_shadenode = manager_nodegroup_MRTKstandard.setting_node_MRTKStandard_ui(arg_node=make_shadenode)

    return make_shadenode

# 指定のオブジェクトに設定されたマテリアルが全てがMRTKStandardかチェックする
def check_object_materials(arg_object:bpy.types.Object) -> bool:
    """指定のオブジェクトに設定されたマテリアルが全てがMRTKStandardかチェックする

    Args:
        arg_object (bpy.types.Object): 指定オブジェクト

    Returns:
        bool: 全てMRTKStandardが設定されているか
    """

    # チェック結果を取得する変数
    all_MRTKstanderd = True

    # 指定オブジェクトのマテリアルリストを取得する
    for material_slot in arg_object.material_slots:
        # スロットのマテリアルを取得する
        target_material = material_slot.material

        # マテリアルが割り当てられているか
        if target_material == None:
            # マテリアルが割り当てられていないマテリアルスロットは無視する
            continue
        
        # ノードが有効かチェックする
        if target_material.use_nodes == False:
            # ノードが有効でないマテリアルがある場合はFalseでチェックを終了する
            all_MRTKstanderd = False
            break

        # アクティブな出力ノードに接続されたノードを取得する
        get_node = get_node_linkoutput(arg_material=target_material)

        # ノードが取得できたか確認する
        if get_node == None:
            # サーフェスノードが存在しないマテリアルがある場合はFalseでチェックを終了する
            all_MRTKstanderd = False
            break

        # ノードの種類がMRTKStandardチェックする
        isMRTKStandard = manager_nodegroup_MRTKstandard.check_isnode_MRTKStandardNode(arg_node=get_node)

        # ノードの種類がMRTKStandardか確認する
        if isMRTKStandard == False:
            # MRTKStandardでないマテリアルがある場合はFalseでチェックを終了する
            all_MRTKstanderd = False
            break

    return all_MRTKstanderd

# 指定マテリアルのアクティブな出力ノードに接続されたノードがMRTKStandardかチェックする
def check_surface_MRTKStandard(arg_material:bpy.types.Material) -> bool:
    """指定マテリアルのアクティブな出力ノードに接続されたノードがMRTKStandardかチェックする

    Args:
        arg_material (bpy.types.Material): 指定マテリアル

    Returns:
        bool: MRTKStandardが接続されているか
    """

    # ノードが有効かチェックする
    if arg_material.use_nodes == False:
        # ノードが有効でない場合はFalseを返す
        return False

    # アクティブな出力ノードに接続されたノードを取得する
    get_node = get_node_linkoutput(arg_material=arg_material)

    # ノードが取得できたか確認する
    if get_node == None:
        # サーフェスノードが存在しない場合はFalseを返す
        return False

    # ノードの種類がMRTKStandardチェックして結果を返す
    isMRTKStandard = manager_nodegroup_MRTKstandard.check_isnode_MRTKStandardNode(arg_node=get_node)

    return isMRTKStandard

# 指定マテリアルのアクティブな出力ノードに接続されたノードがMRTKStandardで透過が0以上かチェックする
def check_trans_MRTKStandard(arg_material:bpy.types.Material) -> bool:
    """指定マテリアルのアクティブな出力ノードに接続されたノードがMRTKStandardで透過が0以上かチェックする

    Args:
        arg_material (bpy.types.Material): 指定マテリアル

    Returns:
        bool: MRTKStandardで透過が0以上か
    """

    # ノードが有効かチェックする
    if arg_material.use_nodes == False:
        # ノードが有効でない場合はFalseを返す
        return False

    # アクティブな出力ノードに接続されたノードを取得する
    get_node = get_node_linkoutput(arg_material=arg_material)

    # ノードが取得できたか確認する
    if get_node == None:
        # サーフェスノードが存在しない場合はFalseを返す
        return False

    # MRTKStandardの透過値が0以上かチェックする
    isTrans = manager_nodegroup_MRTKstandard.check_trans_MRTKStandardNode(arg_node=get_node)

    return isTrans

# MRTKStandardの構成をデフォルトの状態にリセットする
def setting_MRTKStandardNodeGroup_reset() -> bool:
    """MRTKStandardの構成をデフォルトの状態にリセットする

    Returns:
        bool: 実行正否
    """

    # MRTKStandard設定を構成するノードグループのノードリンクを作成する
    setting_result = manager_nodegroup_MRTKstandard.link_MRTKStandardNodeGroup_default()

    return setting_result

# MRTKStandardの構成をカラーベイク用の状態にリセットする
def setting_MRTKStandardNodeGroup_bake_color_mode() -> bool:
    """MRTKStandardの構成をカラーベイク用の状態にリセットする

    Returns:
        bool: 実行正否
    """

    # MRTKStandardのシンプルカラーの接続を切り替える
    setting_result = manager_nodegroup_MRTKstandard.link_MRTKStandardNodeGroup_switch_simple_color()

    return setting_result

# MRTKStandardの構成を滑らかさベイク用の状態にリセットする
def setting_MRTKStandardNodeGroup_bake_smoothness_mode() -> bool:
    """MRTKStandardの構成を滑らかさベイク用の状態にリセットする

    Returns:
        bool: 実行正否
    """

    # 指定ノードのMRTKStandardの滑らかと粗さの反転接続を切り替える
    setting_result = manager_nodegroup_MRTKstandard.link_MRTKStandardNodeGroup_inversion_smoothness_roughness()

    return setting_result

# MRTKStandardの構成をメタリックベイク用の状態にリセットする
def setting_MRTKStandardNodeGroup_bake_metallic_mode() -> bool:
    """MRTKStandardの構成をメタリックベイク用の状態にリセットする

    Returns:
        bool: 実行正否
    """

    # 指定ノードのMRTKStandardのメタリックと粗さの接続を切り替える
    setting_result = manager_nodegroup_MRTKstandard.link_MRTKStandardNodeGroup_cross_metallic_roughness()

    return setting_result

# MRTKStandardの構成をモノクロ放射ベイク用の状態にリセットする
def setting_MRTKStandardNodeGroup_bake_whiteemission_mode() -> bool:
    """MRTKStandardの構成をモノクロ放射ベイク用の状態にリセットする

    Returns:
        bool: 実行正否
    """

    # 指定ノードのMRTKStandardのカラーとRGBミックスの接続有無を切り替える
    setting_result = manager_nodegroup_MRTKstandard.link_MRTKStandardNodeGroup_joint_color_rgbmix()

    return setting_result


# アクティブな出力ノードに接続されたノードを取得する
def get_node_linkoutput(arg_material:bpy.types.Material) -> bpy.types.Node:
    """アクティブな出力ノードに接続されたノードを取得する

    Args:
        arg_material (bpy.types.Material): 指定マテリアル

    Returns:
        bpy.types.Node: アクティブな出力ノードに接続されたノード
    """

    # 参照の保存用変数
    name_mapping = {}

    # ノード操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.Node.html)
    # ノードリスト操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.Nodes.html)
    # ノードツリー操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.NodeTree.html)

    # ターゲットマテリアルのノード参照を取得する
    mat_nodes = arg_material.node_tree.nodes

    # 出力ノードを取得する変数
    output_node = None

    # 出力ノードの操作マニュアル
    # (https://docs.blender.org/api/current/bpy.types.ShaderNodeOutputMaterial.html)

    # 全ノードを走査する
    for check_node in mat_nodes:
        # ノードタイプを取得する
        node_idname = check_node.bl_idname

        # ノードタイプが出力ノードか確認する
        if node_idname == 'ShaderNodeOutputMaterial':
            # アクティブな出力ノードのフラグを取得する
            is_activeoutput = check_node.is_active_output

            # アクティブな出力ノードかチェックする
            if is_activeoutput == True:
                # アクティブな出力ノードなら保持する
                output_node = check_node

    # 出力ノードが取得できたか確認する
    if output_node == None:
        # 出力ノードが存在しない場合は処理しない
        return None
    
    # ノードソケット操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.NodeSocket.html)

    # 出力ノードのサーフェス入力(1番目の入力)のリンクを確認する
    surface_input = output_node.inputs[0]

    # リンクが接続されているか確認する
    if surface_input.is_linked == False:
        # 出力ノードにサーフェスノードが接続されていない場合は処理しない
        return None

    # リンク操作のマニュアル
    # (https://docs.blender.org/api/current/bpy.types.NodeLink.html#bpy.types.NodeLink)

    # リンクの一覧を取得する
    mat_links = arg_material.node_tree.links

    # 接続元ノードを取得する変数
    surface_node = None

    # リンクを走査する
    for check_link in mat_links:
        # 接続先が出力ノードのサーフェス入力か確認する
        if check_link.to_socket == surface_input:
            # リンクの接続元ノードを取得する
            surface_node = check_link.from_node
    
    # 接続元ノードが取得できたか確認する
    if surface_node == None:
        # 接続元ノードが存在しない場合は処理しない
        return None
    
    # 接続元となっているサーフェスノードを返却する
    return_node = surface_node

    return return_node
