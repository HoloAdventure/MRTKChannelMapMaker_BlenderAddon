# bpyインポート
import bpy

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
        isMRTKStandard = check_isnode_MRTKStandardNode(arg_node=get_node)

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
    isMRTKStandard = check_isnode_MRTKStandardNode(arg_node=get_node)

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
    isTrans = check_trans_MRTKStandardNode(arg_node=get_node)

    return isTrans

# 指定マテリアルのアクティブな出力ノードに接続されたMRTKStandardのシンプルカラーの接続を切り替える
def link_switch_simple_color_MRTKStandard(arg_material:bpy.types.Material, arg_simplecolor:bool=False) -> bool:
    """指定マテリアルのアクティブな出力ノードに接続されたMRTKStandardのシンプルカラーの接続を切り替える

    Args:
        arg_material (bpy.types.Material): 指定マテリアル
        arg_simplecolor (bool): シンプルカラーにするか否か

    Returns:
        bool: 実行正否
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

    # MRTKStandardのシンプルカラーの接続を切り替える
    isResult = link_switch_simple_color_MRTKStandardNode(arg_node=get_node, arg_simplecolor=arg_simplecolor)

    return isResult

# 指定マテリアルのアクティブな出力ノードに接続されたMRTKStandardの滑らかさと粗さの反転接続を切り替える
def link_inversion_smoothness_roughness_MRTKStandard(arg_material:bpy.types.Material, arg_uninversion:bool=False) -> bool:
    """指定マテリアルのアクティブな出力ノードに接続されたMRTKStandardの滑らかさと粗さの反転接続を切り替える

    Args:
        arg_material (bpy.types.Material): 指定マテリアル
        arg_uninversion (bool): 反転させないか否か

    Returns:
        bool: 実行正否
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

    # MRTKStandardの滑らかさと粗さの反転接続を切り替える
    isResult = link_inversion_smoothness_roughness_MRTKStandardNode(arg_node=get_node, arg_uninversion=arg_uninversion)

    return isResult

# 指定マテリアルのアクティブな出力ノードに接続されたMRTKStandardのメタリックと粗さの接続を切り替える
def link_cross_metallic_roughness_MRTKStandard(arg_material:bpy.types.Material, arg_cross:bool=False) -> bool:
    """指定マテリアルのアクティブな出力ノードに接続されたMRTKStandardのメタリックと粗さの接続を切り替える

    Args:
        arg_material (bpy.types.Material): 指定マテリアル
        arg_cross (bool): 交差させるか否か

    Returns:
        bool: 実行正否
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

    # MRTKStandardのメタリックと粗さの接続を切り替える
    isResult = link_cross_metallic_roughness_MRTKStandardNode(arg_node=get_node, arg_cross=arg_cross)

    return isResult

# 指定マテリアルのアクティブな出力ノードに接続されたMRTKStandardのカラーとrgbミックスの接続有無を切り替える
def link_joint_color_rgbmix_MRTKStandard(arg_material:bpy.types.Material, arg_unjoint:bool=False) -> bool:
    """指定マテリアルのアクティブな出力ノードに接続されたMRTKStandardのカラーとrgbミックスの接続有無を切り替える

    Args:
        arg_material (bpy.types.Material): 指定マテリアル
        arg_unjoint (bool): リンク解除するか否か

    Returns:
        bool: 実行正否
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

    # MRTKStandardのカラーとrgbミックスの接続有無を切り替える
    isResult = link_joint_color_rgbmix_MRTKStandardNode(arg_node=get_node, arg_unjoint=arg_unjoint)

    return isResult



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

# 指定ノードがMRTKStandardで透過が0以上かチェックする
def check_trans_MRTKStandardNode(arg_node:bpy.types.Node) -> bool:
    """指定ノードがMRTKStandardかチェックする

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
    input_trans = arg_node.inputs['Transmission']
    trans_val = input_trans.default_value

    # チェック結果
    isTrans = False

    # 透過の入力値が0以上か確認する
    if trans_val > 0:
        # 0以上であれば透過設定と判定する
        isTrans = True
        
    return isTrans

# 指定ノードのMRTKStandardのシンプルカラーの接続を切り替える
def link_switch_simple_color_MRTKStandardNode(arg_node:bpy.types.Node, arg_simplecolor:bool=False) -> bool:
    """指定ノードのMRTKStandardのシンプルカラーの接続を切り替える

    Args:
        arg_node (bpy.types.Node): 指定ノード
        arg_simplecolor (bool): シンプルカラーにするか否か

    Returns:
        bool: 実行正否
    """

    # 入力ノード名を定義する
    inputnode_name = "MRTKStandardInputNode"

    # プリンシプルBSDFノード名を定義する
    bsdfnode_name = "MRTKStandardBSDFNode"

    # RGBミックスノード名を定義する
    rgbmixnode_name = "MRTKStandardRGBMix"

    # 滑らかさ数値反転ノード名を定義する
    smoothinversionnode_name = "MRTKStandardSmoothInversion"

    # ノードの種類がMRTKStandardチェックする
    isMRTKStandard = check_isnode_MRTKStandardNode(arg_node)

    # MRTKStandardか確認する
    if isMRTKStandard == False:
        # MRTKStandardでない場合はFalseを返す
        return False

    # ノードグループを取得する
    mrtkstandard_nodegroup = arg_node.node_tree

    # リンクリストを取得する
    mrtkstandard_links = mrtkstandard_nodegroup.links

    # ノードグループ内の入力ノードを取得する
    mrtkstandard_inputnode = mrtkstandard_nodegroup.nodes[inputnode_name]

    # ノードグループ内のBSDFノードを取得する
    mrtkstandard_bsdfnode = mrtkstandard_nodegroup.nodes[bsdfnode_name]

    # ノードグループ内のRGBミックスノードを取得する
    mrtkstandard_rgbmixnode = mrtkstandard_nodegroup.nodes[rgbmixnode_name]

    # ノードグループ内の滑らかさ数値反転ノードを取得する
    mrtkstandard_smoothinversionnode = mrtkstandard_nodegroup.nodes[smoothinversionnode_name]

    # BSDFノードのベースカラーに接続された全てのリンクを走査する
    for link in mrtkstandard_bsdfnode.inputs['Base Color'].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)
    
    # BSDFノードのメタリックに接続された全てのリンクを走査する
    for link in mrtkstandard_bsdfnode.inputs['Metallic'].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)

    # BSDFノードの粗さに接続された全てのリンクを走査する
    for link in mrtkstandard_bsdfnode.inputs['Roughness'].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)
        
    # BSDFノードの伝播に接続された全てのリンクを走査する
    for link in mrtkstandard_bsdfnode.inputs['Transmission'].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)
        
    # BSDFノードの放射に接続された全てのリンクを走査する
    for link in mrtkstandard_bsdfnode.inputs['Emission'].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)
        
    # BSDFノードのノーマルに接続された全てのリンクを走査する
    for link in mrtkstandard_bsdfnode.inputs['Normal'].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)

    if arg_simplecolor == True:
        # ベースカラーのみ再接続する
        # (inputベースカラー -> bsdfベースカラー)
        mrtkstandard_links.new(mrtkstandard_inputnode.outputs['Base Color'], mrtkstandard_bsdfnode.inputs['Base Color'])
    else:
        # 通常の接続に戻す
        # (inputベースカラー -> bsdfベースカラー)
        mrtkstandard_links.new(mrtkstandard_inputnode.outputs['Base Color'], mrtkstandard_bsdfnode.inputs['Base Color'])
    
        # メタリック
        # (inputメタリック -> bsdfメタリック)
        mrtkstandard_links.new(mrtkstandard_inputnode.outputs['Metallic'], mrtkstandard_bsdfnode.inputs['Metallic'])
    
        # 透過
        # (input透過 -> bsdf伝播)
        mrtkstandard_links.new(mrtkstandard_inputnode.outputs['Transmission'], mrtkstandard_bsdfnode.inputs['Transmission'])

        # ノーマル
        # (inputノーマル -> bsdfノーマル)
        mrtkstandard_links.new(mrtkstandard_inputnode.outputs['Normal'], mrtkstandard_bsdfnode.inputs['Normal'])

        # 放射
        # (input放射 -> rgbmix係数)
        mrtkstandard_links.new(mrtkstandard_rgbmixnode.outputs['Color'], mrtkstandard_bsdfnode.inputs['Emission'])

        # 粗さ
        # (smoothinversion出力 -> bsdf粗さ)
        mrtkstandard_links.new(mrtkstandard_smoothinversionnode.outputs['Value'], mrtkstandard_bsdfnode.inputs['Roughness'])
        
    return True

# 指定ノードのMRTKStandardの滑らかと粗さの反転接続を切り替える
def link_inversion_smoothness_roughness_MRTKStandardNode(arg_node:bpy.types.Node, arg_uninversion:bool=False) -> bool:
    """指定ノードのMRTKStandardの滑らかと粗さの反転接続を切り替える

    Args:
        arg_node (bpy.types.Node): 指定ノード
        arg_uninversion (bool): 反転させないか否か

    Returns:
        bool: 実行正否
    """

    # 入力ノード名を定義する
    inputnode_name = "MRTKStandardInputNode"

    # プリンシプルBSDFノード名を定義する
    bsdfnode_name = "MRTKStandardBSDFNode"

    # 滑らかさ数値反転ノード名を定義する
    smoothinversionnode_name = "MRTKStandardSmoothInversion"

    # ノードの種類がMRTKStandardチェックする
    isMRTKStandard = check_isnode_MRTKStandardNode(arg_node)

    # MRTKStandardか確認する
    if isMRTKStandard == False:
        # MRTKStandardでない場合はFalseを返す
        return False

    # ノードグループを取得する
    mrtkstandard_nodegroup = arg_node.node_tree

    # リンクリストを取得する
    mrtkstandard_links = mrtkstandard_nodegroup.links

    # ノードグループ内の入力ノードを取得する
    mrtkstandard_inputnode = mrtkstandard_nodegroup.nodes[inputnode_name]

    # ノードグループ内のBSDFノードを取得する
    mrtkstandard_bsdfnode = mrtkstandard_nodegroup.nodes[bsdfnode_name]

    # ノードグループ内の滑らかさ数値反転ノードを取得する
    mrtkstandard_smoothinversionnode = mrtkstandard_nodegroup.nodes[smoothinversionnode_name]

    # 入力ノードの滑らかさに接続された全てのリンクを走査する
    for link in mrtkstandard_inputnode.outputs['Smoothness'].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)

    # 滑らかさ数値反転ノードの出力に接続された全てのリンクを走査する
    for link in mrtkstandard_smoothinversionnode.outputs['Value'].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)

    if arg_uninversion == True:
        # 滑らかさと粗さを反転しないで接続する
        # (input滑らかさ -> smoothinversion端子２)
        mrtkstandard_links.new(mrtkstandard_inputnode.outputs['Smoothness'], mrtkstandard_bsdfnode.inputs['Roughness'])
    else:
        # 滑らかさと粗さを反転して接続する
        # (input滑らかさ -> smoothinversion端子２)
        mrtkstandard_links.new(mrtkstandard_inputnode.outputs['Smoothness'], mrtkstandard_smoothinversionnode.inputs[1])

        # (smoothinversion出力 -> bsdf粗さ)
        mrtkstandard_links.new(mrtkstandard_smoothinversionnode.outputs['Value'], mrtkstandard_bsdfnode.inputs['Roughness'])
        
    return True

# 指定ノードのMRTKStandardのメタリックと粗さの接続を切り替える
def link_cross_metallic_roughness_MRTKStandardNode(arg_node:bpy.types.Node, arg_cross:bool=False) -> bool:
    """指定ノードのMRTKStandardのメタリックと粗さの接続を切り替える

    Args:
        arg_node (bpy.types.Node): 指定ノード
        arg_cross (bool): 交差させるか否か

    Returns:
        bool: 実行正否
    """

    # 入力ノード名を定義する
    inputnode_name = "MRTKStandardInputNode"

    # プリンシプルBSDFノード名を定義する
    bsdfnode_name = "MRTKStandardBSDFNode"

    # 滑らかさ数値反転ノード名を定義する
    smoothinversionnode_name = "MRTKStandardSmoothInversion"

    # ノードの種類がMRTKStandardチェックする
    isMRTKStandard = check_isnode_MRTKStandardNode(arg_node)

    # MRTKStandardか確認する
    if isMRTKStandard == False:
        # MRTKStandardでない場合はFalseを返す
        return False

    # ノードグループを取得する
    mrtkstandard_nodegroup = arg_node.node_tree

    # リンクリストを取得する
    mrtkstandard_links = mrtkstandard_nodegroup.links

    # ノードグループ内の入力ノードを取得する
    mrtkstandard_inputnode = mrtkstandard_nodegroup.nodes[inputnode_name]

    # ノードグループ内のBSDFノードを取得する
    mrtkstandard_bsdfnode = mrtkstandard_nodegroup.nodes[bsdfnode_name]

    # ノードグループ内の滑らかさ数値反転ノードを取得する
    mrtkstandard_smoothinversionnode = mrtkstandard_nodegroup.nodes[smoothinversionnode_name]

    # 入力ノードのメタリックに接続された全てのリンクを走査する
    for link in mrtkstandard_inputnode.outputs['Metallic'].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)

    # 入力ノードの粗さに接続された全てのリンクを走査する
    for link in mrtkstandard_inputnode.outputs['Smoothness'].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)

    if arg_cross == True:
        # メタリックと粗さを交差して接続する
        # (inputメタリック -> bsdf粗さ)
        mrtkstandard_links.new(mrtkstandard_inputnode.outputs['Metallic'], mrtkstandard_bsdfnode.inputs['Roughness'])
        
        # (input滑らかさ -> smoothinversion端子２)
        mrtkstandard_links.new(mrtkstandard_inputnode.outputs['Smoothness'], mrtkstandard_smoothinversionnode.inputs[1])

        # (smoothinversion出力 -> bsdfメタリック)
        mrtkstandard_links.new(mrtkstandard_smoothinversionnode.outputs['Value'], mrtkstandard_bsdfnode.inputs['Metallic'])
    else:
        # メタリックと粗さを正しく接続する
        # (inputメタリック -> bsdfメタリック)
        mrtkstandard_links.new(mrtkstandard_inputnode.outputs['Metallic'], mrtkstandard_bsdfnode.inputs['Metallic'])
        
        # (input滑らかさ -> smoothinversion端子２)
        mrtkstandard_links.new(mrtkstandard_inputnode.outputs['Smoothness'], mrtkstandard_smoothinversionnode.inputs[1])

        # (smoothinversion出力 -> bsdf粗さ)
        mrtkstandard_links.new(mrtkstandard_smoothinversionnode.outputs['Value'], mrtkstandard_bsdfnode.inputs['Roughness'])
        
    return True

# 指定ノードのMRTKStandardのカラーとRGBミックスの接続有無を切り替える
def link_joint_color_rgbmix_MRTKStandardNode(arg_node:bpy.types.Node, arg_unjoint:bool=False) -> bool:
    """指定ノードのMRTKStandardのカラーとRGBミックスの接続有無を切り替える

    Args:
        arg_node (bpy.types.Node): 指定ノード
        arg_unjoint (bool): リンク解除するか否か

    Returns:
        bool: 実行正否
    """

    # 入力ノード名を定義する
    inputnode_name = "MRTKStandardInputNode"

    # プリンシプルBSDFノード名を定義する
    bsdfnode_name = "MRTKStandardBSDFNode"

    # RGBミックスノード名を定義する
    rgbmixnode_name = "MRTKStandardRGBMix"

    # ノードの種類がMRTKStandardチェックする
    isMRTKStandard = check_isnode_MRTKStandardNode(arg_node)

    # MRTKStandardか確認する
    if isMRTKStandard == False:
        # MRTKStandardでない場合はFalseを返す
        return False

    # ノードグループを取得する
    mrtkstandard_nodegroup = arg_node.node_tree

    # リンクリストを取得する
    mrtkstandard_links = mrtkstandard_nodegroup.links

    # ノードグループ内の入力ノードを取得する
    mrtkstandard_inputnode = mrtkstandard_nodegroup.nodes[inputnode_name]

    # ノードグループ内のBSDFノードを取得する
    mrtkstandard_bsdfnode = mrtkstandard_nodegroup.nodes[bsdfnode_name]

    # ノードグループ内のRGBミックスノードを取得する
    mrtkstandard_rgbmixfnode = mrtkstandard_nodegroup.nodes[rgbmixnode_name]

    # 入力ノードのベースカラーに接続された全てのリンクを走査する
    for link in mrtkstandard_inputnode.outputs['Base Color'].links:
        # 接続リンクをリストから削除する
        mrtkstandard_links.remove(link)

    if arg_unjoint == True:
        # RGBノードのベースカラーのみ再接続する
        # (inputベースカラー -> bsdfベースカラー)
        mrtkstandard_links.new(mrtkstandard_inputnode.outputs['Base Color'], mrtkstandard_bsdfnode.inputs['Base Color'])
    else:
        # RGBノードのベースカラーとRGBミックスに再接続する
        # (inputベースカラー -> bsdfベースカラー)
        mrtkstandard_links.new(mrtkstandard_inputnode.outputs['Base Color'], mrtkstandard_bsdfnode.inputs['Base Color'])
        # (inputベースカラー -> rgbmixカラー2)
        mrtkstandard_links.new(mrtkstandard_inputnode.outputs['Base Color'], mrtkstandard_rgbmixfnode.inputs['Color2'])
        
    return True


# 指定ノードがMRTKStandardかチェックする
def check_isnode_MRTKStandardNode(arg_node:bpy.types.Node) -> bool:
    """指定ノードがMRTKStandardかチェックする

    Args:
        arg_node (bpy.types.Node): 指定ノード

    Returns:
        bool: MRTKStandardか否か
    """

    # ノードグループ名を定義する
    nodegroup_name = "MRTKStandardNodeGroup"

    # チェック結果
    isMRTKStandard = False

    # ノードタイプを取得する
    node_idname = arg_node.bl_idname

    # ノードタイプがノードグループか確認する
    if node_idname == 'ShaderNodeGroup':
        # ノードグループならツリー情報(ノードグループ)の名前を取得する
        nodetree_name = arg_node.node_tree.name

        # ノードグループのツリー名称が定義と一致するか確認する
        if nodetree_name == nodegroup_name:
            # 一致すればMRTKStandardと判定する
            isMRTKStandard = True

    return isMRTKStandard

