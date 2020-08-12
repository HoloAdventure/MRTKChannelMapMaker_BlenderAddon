# 各種ライブラリインポート
if "bpy" in locals():
    import importlib
    if "UI_operations" in locals():
        importlib.reload(UI_operations)
import bpy
from . import UI_operations

# bl_infoでプラグインに関する情報の定義を行う
bl_info = {
    "name": "HoloMon MRTK ChannelMap Maker Addon",   # プラグイン名
    "author": "HoloMon",                             # 制作者名
    "version": (1, 7),                               # バージョン
    "blender": (2, 80, 0),                           # 動作可能なBlenderバージョン
    "support": "TESTING",                            # サポートレベル
    "category": "Properties",                        # カテゴリ名
    "location": "Properties > Material > HoloMon",   # ロケーション
    "description": "Addon MRTK ChannelMap Maker",    # 説明文
    "location": "",                                  # 機能の位置付け
    "warning": "",                                   # 注意点やバグ情報
    "doc_url": "",                                   # ドキュメントURL
}

# 利用するタイプやメソッドのインポート
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import PointerProperty, BoolProperty, IntProperty, FloatProperty, StringProperty

# 継承するクラスの命名規則は以下の通り
# [A-Z][A-Z0-9_]*_(継承クラスごとの識別子)_[A-Za-z0-9_]+
# クラスごとの識別子は以下の通り
#   bpy.types.Operator  OT
#   bpy.types.Panel     PT
#   bpy.types.Header    HT
#   bpy.types.MENU      MT
#   bpy.types.UIList    UL

# Panelクラスの作成
# 参考URL:https://docs.blender.org/api/current/bpy.types.Panel.html
# マテリアル追加の実行パネル(プロパティ)
class HOLOMON_PT_addon_mrtk_material_maker(Panel):
    # パネルのラベル名を定義する
    # パネルを折りたたむパネルヘッダーに表示される
    bl_label = "MRTK Material Maker"
    # クラスのIDを定義する
    # 命名規則は CATEGORY_PT_name
    bl_idname = "HOLOMON_PT_mrtk_material_maker"
    # パネルを使用する領域を定義する
    # 利用可能な識別子は以下の通り
    #   EMPTY：無し
    #   VIEW_3D：3Dビューポート
    #   IMAGE_EDITOR：UV/画像エディター
    #   NODE_EDITOR：ノードエディター
    #   SEQUENCE_EDITOR：ビデオシーケンサー
    #   CLIP_EDITOR：ムービークリップエディター
    #   DOPESHEET_EDITOR：ドープシート
    #   GRAPH_EDITOR：グラフエディター
    #   NLA_EDITOR：非線形アニメーション
    #   TEXT_EDITOR：テキストエディター
    #   CONSOLE：Pythonコンソール
    #   INFO：情報、操作のログ、警告、エラーメッセージ
    #   TOPBAR：トップバー
    #   STATUSBAR：ステータスバー
    #   OUTLINER：アウトライナ
    #   PROPERTIES：プロパティ
    #   FILE_BROWSER：ファイルブラウザ
    #   PREFERENCES：設定
    bl_space_type = 'PROPERTIES'
    # 表示領域のコンテンツを定義する
    bl_context = 'material'
    # パネルが使用される領域を定義する
    # 利用可能な識別子は以下の通り
    # ['WINDOW'、 'HEADER'、 'CHANNELS'、 'TEMPORARY'、 'UI'、
    #  'TOOLS'、 'TOOL_PROPS'、 'PREVIEW'、 'HUD'、 'NAVIGATION_BAR'、
    #  'EXECUTE'、 'FOOTER'の列挙型、 'TOOL_HEADER']
    bl_region_type = 'WINDOW'
    # パネルタイプのオプションを定義する
    # DEFAULT_CLOSED：作成時にパネルを開くか折りたたむ必要があるかを定義する。
    # HIDE_HEADER：ヘッダーを非表示するかを定義する。Falseに設定するとパネルにはヘッダーが表示される。
    # デフォルトは {'DEFAULT_CLOSED'}
    bl_options = {'DEFAULT_CLOSED'}
    # パネルの表示順番を定義する
    # 小さい番号のパネルは、大きい番号のパネルの前にデフォルトで順序付けられる
    # デフォルトは 0
    bl_order = 255
    # パネルのカテゴリ名称を定義する
    # 3Dビューポートの場合、サイドバーの名称になる
    # デフォルトは名称無し
    bl_category = "MRTK"
 
    # 描画の定義
    def draw(self, context):
        # Operatorをボタンとして配置する
        draw_layout = self.layout
        # 要素行を作成する
        button_row = draw_layout.row()
        # マテリアル追加を実行するボタンを配置する
        button_row.operator("holomon.mrtk_material_maker")

# マテリアルベイクの実行パネル(3Dビュー)
class HOLOMON_PT_addon_mrtk_channelmap_maker(Panel):
    # パネルのラベル名を定義する
    # パネルを折りたたむパネルヘッダーに表示される
    bl_label = "MRTK ChannelMap Maker"
    # クラスのIDを定義する
    # 命名規則は CATEGORY_PT_name
    bl_idname = "HOLOMON_PT_addon_mrtk_channelmap_maker"
    # パネルを使用する領域を定義する
    # 利用可能な識別子は以下の通り
    #   EMPTY：無し
    #   VIEW_3D：3Dビューポート
    #   IMAGE_EDITOR：UV/画像エディター
    #   NODE_EDITOR：ノードエディター
    #   SEQUENCE_EDITOR：ビデオシーケンサー
    #   CLIP_EDITOR：ムービークリップエディター
    #   DOPESHEET_EDITOR：ドープシート
    #   GRAPH_EDITOR：グラフエディター
    #   NLA_EDITOR：非線形アニメーション
    #   TEXT_EDITOR：テキストエディター
    #   CONSOLE：Pythonコンソール
    #   INFO：情報、操作のログ、警告、エラーメッセージ
    #   TOPBAR：トップバー
    #   STATUSBAR：ステータスバー
    #   OUTLINER：アウトライナ
    #   PROPERTIES：プロパティ
    #   FILE_BROWSER：ファイルブラウザ
    #   PREFERENCES：設定
    bl_space_type = 'VIEW_3D'
    # パネルが使用される領域を定義する
    # 利用可能な識別子は以下の通り
    # ['WINDOW'、 'HEADER'、 'CHANNELS'、 'TEMPORARY'、 'UI'、
    #  'TOOLS'、 'TOOL_PROPS'、 'PREVIEW'、 'HUD'、 'NAVIGATION_BAR'、
    #  'EXECUTE'、 'FOOTER'の列挙型、 'TOOL_HEADER']
    bl_region_type = 'UI'
    # パネルタイプのオプションを定義する
    # DEFAULT_CLOSED：作成時にパネルを開くか折りたたむ必要があるかを定義する。
    # HIDE_HEADER：ヘッダーを非表示するかを定義する。Falseに設定するとパネルにはヘッダーが表示される。
    # デフォルトは {'DEFAULT_CLOSED'}
    bl_options = {'DEFAULT_CLOSED'}
    # パネルの表示順番を定義する
    # 小さい番号のパネルは、大きい番号のパネルの前にデフォルトで順序付けられる
    # デフォルトは 0
    bl_order = 0
    # パネルのカテゴリ名称を定義する
    # 3Dビューポートの場合、サイドバーの名称になる
    # デフォルトは名称無し
    bl_category = "MRTK"
 
    # 描画の定義
    def draw(self, context):
        # Operatorをボタンとして配置する
        draw_layout = self.layout

        # 要素行を作成する
        objectslect_row = draw_layout.row()
        # オブジェクト選択用のカスタムプロパティを配置する
        objectslect_row.prop(context.scene.holomon_mrtk_channelmap_maker, "prop_objectslect", text="Target")
        # 要素行を作成する
        texturename_row = draw_layout.row()
        # テクスチャ名指定用のカスタムプロパティを配置する
        texturename_row.prop(context.scene.holomon_mrtk_channelmap_maker, "prop_texturename", text="")
        # 要素行を作成する
        colortexturesize_row = draw_layout.row()
        # カラーテクスチャサイズ指定用のカスタムプロパティを配置する
        colortexturesize_row.prop(context.scene.holomon_mrtk_channelmap_maker, "prop_colortexturesize")
        # 要素行を作成する
        bakemargin_row = draw_layout.row()
        # ベイク余白指定用のカスタムプロパティを配置する
        bakemargin_row.prop(context.scene.holomon_mrtk_channelmap_maker, "prop_bakemargin")

        # 要素行を作成する
        baketo_newsmartuv_row = draw_layout.row()
        # 新規スマートUV作成実行用のカスタムプロパティを配置する
        baketo_newsmartuv_row.prop(context.scene.holomon_mrtk_channelmap_maker, "prop_baketo_newsmartuv")

        # 要素行を作成する
        button_row = draw_layout.row()
        # ベイクを実行するボタンを配置する
        button_row.operator("holomon.mrtk_channelmap_maker", icon='FILE_IMAGE')

# マテリアルベイクのオプションパネル(3Dビュー)
class HOLOMON_PT_addon_mrtk_channelmap_maker_option(Panel):
    # パネルのラベル名を定義する
    # パネルを折りたたむパネルヘッダーに表示される
    bl_label = "MRTK ChannelMap Options"
    # クラスのIDを定義する
    # 命名規則は CATEGORY_PT_name
    bl_idname = "HOLOMON_PT_addon_mrtk_channelmap_maker_option"
    # パネルを使用する領域を定義する
    # 利用可能な識別子は以下の通り
    #   EMPTY：無し
    #   VIEW_3D：3Dビューポート
    #   IMAGE_EDITOR：UV/画像エディター
    #   NODE_EDITOR：ノードエディター
    #   SEQUENCE_EDITOR：ビデオシーケンサー
    #   CLIP_EDITOR：ムービークリップエディター
    #   DOPESHEET_EDITOR：ドープシート
    #   GRAPH_EDITOR：グラフエディター
    #   NLA_EDITOR：非線形アニメーション
    #   TEXT_EDITOR：テキストエディター
    #   CONSOLE：Pythonコンソール
    #   INFO：情報、操作のログ、警告、エラーメッセージ
    #   TOPBAR：トップバー
    #   STATUSBAR：ステータスバー
    #   OUTLINER：アウトライナ
    #   PROPERTIES：プロパティ
    #   FILE_BROWSER：ファイルブラウザ
    #   PREFERENCES：設定
    bl_space_type = 'VIEW_3D'
    # パネルが使用される領域を定義する
    # 利用可能な識別子は以下の通り
    # ['WINDOW'、 'HEADER'、 'CHANNELS'、 'TEMPORARY'、 'UI'、
    #  'TOOLS'、 'TOOL_PROPS'、 'PREVIEW'、 'HUD'、 'NAVIGATION_BAR'、
    #  'EXECUTE'、 'FOOTER'の列挙型、 'TOOL_HEADER']
    bl_region_type = 'UI'
    # パネルタイプのオプションを定義する
    # DEFAULT_CLOSED：作成時にパネルを開くか折りたたむ必要があるかを定義する。
    # HIDE_HEADER：ヘッダーを非表示するかを定義する。Falseに設定するとパネルにはヘッダーが表示される。
    # デフォルトは {'DEFAULT_CLOSED'}
    bl_options = {'DEFAULT_CLOSED'}
    # パネルの表示順番を定義する
    # 小さい番号のパネルは、大きい番号のパネルの前にデフォルトで順序付けられる
    # デフォルトは 0
    bl_order = 1
    # パネルのカテゴリ名称を定義する
    # 3Dビューポートの場合、サイドバーの名称になる
    # デフォルトは名称無し
    bl_category = "MRTK"
 
    # 描画の定義
    def draw(self, context):
        # Operatorをボタンとして配置する
        draw_layout = self.layout

        # 要素行を作成する
        baketype_metallic_row = draw_layout.row()
        # メタリックベイク指定用のカスタムプロパティを配置する
        baketype_metallic_row.prop(context.scene.holomon_mrtk_channelmap_maker, "prop_baketype_metallic")
        # 要素行を作成する
        baketype_occlusion_row = draw_layout.row()
        # オクルージョンベイク指定用のカスタムプロパティを配置する
        baketype_occlusion_row.prop(context.scene.holomon_mrtk_channelmap_maker, "prop_baketype_occlusion")
        # 要素行を作成する
        baketype_emission_row = draw_layout.row()
        # エミッションベイク指定用のカスタムプロパティを配置する
        baketype_emission_row.prop(context.scene.holomon_mrtk_channelmap_maker, "prop_baketype_emission")
        # 要素行を作成する
        baketype_smoothness_row = draw_layout.row()
        # 滑らかさベイク指定用のカスタムプロパティを配置する
        baketype_smoothness_row.prop(context.scene.holomon_mrtk_channelmap_maker, "prop_baketype_smoothness")

        # 要素行を作成する
        channelmapsize_row = draw_layout.row()
        # チャンネルマップサイズ指定用のカスタムプロパティを配置する
        channelmapsize_row.prop(context.scene.holomon_mrtk_channelmap_maker, "prop_channelmapsize")
        # 要素行を作成する
        aofactor_row = draw_layout.row()
        # AO係数指定用のカスタムプロパティを配置する
        aofactor_row.prop(context.scene.holomon_mrtk_channelmap_maker, "prop_aofactor")
        # 要素行を作成する
        aodistance_row = draw_layout.row()
        # AO距離指定用のカスタムプロパティを配置する
        aodistance_row.prop(context.scene.holomon_mrtk_channelmap_maker, "prop_aodistance")

        # 要素行を作成する
        baketype_normal_row = draw_layout.row()
        # ノーマルベイク指定用のカスタムプロパティを配置する
        baketype_normal_row.prop(context.scene.holomon_mrtk_channelmap_maker, "prop_baketype_normal")

        # 要素行を作成する
        normalmapsize_row = draw_layout.row()
        # ノーマルマップサイズ指定用のカスタムプロパティを配置する
        normalmapsize_row.prop(context.scene.holomon_mrtk_channelmap_maker, "prop_normalmapsize")


        # チャンネルマップ関連ベイク指定用のカスタムプロパティの有効無効を確認する
        if not (context.scene.holomon_mrtk_channelmap_maker.prop_baketype_metallic
            or context.scene.holomon_mrtk_channelmap_maker.prop_baketype_occlusion
            or context.scene.holomon_mrtk_channelmap_maker.prop_baketype_emission
            or context.scene.holomon_mrtk_channelmap_maker.prop_baketype_smoothness):
            # チャンネルマップ関連ベイク指定が無効の場合はチャンネルマップ設定の項目を無効化する
            channelmapsize_row.enabled = False

        # オクルージョンベイク指定用のカスタムプロパティの有効無効を確認する
        if not context.scene.holomon_mrtk_channelmap_maker.prop_baketype_occlusion:
            # オクルージョンベイク指定が無効の場合はオクルージョン設定の項目を無効化する
            aofactor_row.enabled = False
            aodistance_row.enabled = False

        # ノーマルマップベイク指定用のカスタムプロパティの有効無効を確認する
        if not context.scene.holomon_mrtk_channelmap_maker.prop_baketype_normal:
            # ノーマルマップベイク指定が無効の場合はオクルージョン設定の項目を無効化する
            normalmapsize_row.enabled = False


# Operatorクラスの作成
# 参考URL:https://docs.blender.org/api/current/bpy.types.Operator.html
# マテリアル追加の実行オペレーター
class HOLOMON_OT_addon_mrtk_material_maker(Operator):
    # クラスのIDを定義する
    # (Blender内部で参照する際のIDに利用)
    bl_idname = "holomon.mrtk_material_maker"
    # クラスのラベルを定義する
    # (デフォルトのテキスト表示などに利用)
    bl_label = "Make MRTK Material"
    # クラスの説明文
    # (マウスオーバー時に表示)
    dl_description = "MRTK Material Make Addon"
    # クラスの属性
    # 以下の属性を設定できる
    #   REGISTER      : Operatorを情報ウィンドウに表示し、やり直しツールバーパネルをサポートする
    #   UNDO          : 元に戻すイベントをプッシュする（Operatorのやり直しに必要）
    #   UNDO_GROUPED  : Operatorの繰り返しインスタンスに対して単一の取り消しイベントをプッシュする
    #   BLOCKING      : 他の操作がマウスポインタ―を使用できないようにブロックする
    #   MACRO         : Operatorがマクロであるかどうかを確認するために使用する
    #   GRAB_CURSOR   : 継続的な操作が有効な場合にオペレーターがマウスポインターの動きを参照して、操作を有効にする
    #   GRAB_CURSOR_X : マウスポインターのX軸の動きのみを参照する
    #   GRAB_CURSOR_Y : マウスポインターのY軸の動きのみを参照する
    #   PRESET        : Operator設定を含むプリセットボタンを表示する
    #   INTERNAL      : 検索結果からOperatorを削除する
    # 参考URL:https://docs.blender.org/api/current/bpy.types.Operator.html#bpy.types.Operator.bl_options
    bl_options = {'REGISTER', 'UNDO'}


    # Operator実行時の処理
    def execute(self, context):
        # シーンのアクティブなオブジェクトを取得する
        # (プロパティのマテリアルタブを開いているオブジェクトに処理を行う)
        target_obj = context.view_layer.objects.active

        # 指定中のオブジェクトを確認する
        if target_obj == None:
            # オブジェクトが指定されていない場合はエラーメッセージを表示する
            self.report({'ERROR'}, "Nothing : No objects selected.")
            return {'CANCELLED'}

        # 指定オブジェクトがメッシュオブジェクトか確認する
        if target_obj.type != 'MESH':
            # メッシュオブジェクトでない場合は処理しない
            self.report({'ERROR'}, "Nothing : No Mesh selected.")
            return {'CANCELLED'}

        # マテリアルを追加する
        error_message = UI_operations.UI_mrtk_material_maker(
            arg_object=target_obj,
            arg_materialname="MRTKStandardMaterial"
        )
        
        # エラーメッセージの有無を確認する
        if error_message != None:
            # エラーメッセージが設定されている場合はエラーメッセージを表示する
            self.report({'ERROR'}, error_message)
            return {'CANCELLED'}

        return {'FINISHED'}

# マテリアルベイクの実行オペレーター
class HOLOMON_OT_addon_mrtk_channelmap_maker(Operator):
    # クラスのIDを定義する
    # (Blender内部で参照する際のIDに利用)
    bl_idname = "holomon.mrtk_channelmap_maker"
    # クラスのラベルを定義する
    # (デフォルトのテキスト表示などに利用)
    bl_label = "Make Textures"
    # クラスの説明文
    # (マウスオーバー時に表示)
    dl_description = "MRTK ChannelMap Maker Addon"
    # クラスの属性
    # 以下の属性を設定できる
    #   REGISTER      : Operatorを情報ウィンドウに表示し、やり直しツールバーパネルをサポートする
    #   UNDO          : 元に戻すイベントをプッシュする（Operatorのやり直しに必要）
    #   UNDO_GROUPED  : Operatorの繰り返しインスタンスに対して単一の取り消しイベントをプッシュする
    #   BLOCKING      : 他の操作がマウスポインタ―を使用できないようにブロックする
    #   MACRO         : Operatorがマクロであるかどうかを確認するために使用する
    #   GRAB_CURSOR   : 継続的な操作が有効な場合にオペレーターがマウスポインターの動きを参照して、操作を有効にする
    #   GRAB_CURSOR_X : マウスポインターのX軸の動きのみを参照する
    #   GRAB_CURSOR_Y : マウスポインターのY軸の動きのみを参照する
    #   PRESET        : Operator設定を含むプリセットボタンを表示する
    #   INTERNAL      : 検索結果からOperatorを削除する
    # 参考URL:https://docs.blender.org/api/current/bpy.types.Operator.html#bpy.types.Operator.bl_options
    bl_options = {'REGISTER', 'UNDO'}


    # ファイル指定のプロパティを定義する
    # filepath, filename, directory の名称のプロパティを用意しておくと
    # window_manager.fileselect_add 関数から情報が代入される
    filepath: StringProperty(
        name="File Path",      # プロパティ名
        default="",            # デフォルト値
        maxlen=1024,           # 最大文字列長
        subtype='FILE_PATH',   # サブタイプ
        description="",        # 説明文
    )
    filename: StringProperty(
        name="File Name",      # プロパティ名
        default="",            # デフォルト値
        maxlen=1024,           # 最大文字列長
        description="",        # 説明文
    )
    directory: StringProperty(
        name="Directory Path", # プロパティ名
        default="",            # デフォルト値
        maxlen=1024,           # 最大文字列長
        subtype='FILE_PATH',   # サブタイプ
        description="",        # 説明文
    )

    # 読み込みの拡張子を指定する
    # filter_glob を指定しておくと window_manager.fileselect_add が拡張子をフィルタする
    filter_glob: StringProperty(
        default="*.blend",        # デフォルト値
        options={'HIDDEN'},       # オプション設定
    )


    # 実行時イベント
    def invoke(self, context, event):
        # ファイルエクスプローラーを表示する
        # 参考URL:https://docs.blender.org/api/current/bpy.types.WindowManager.html#bpy.types.WindowManager.fileselect_add
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    # Operator実行時の処理
    def execute(self, context):
        # カスタムプロパティからカラーベイクの実行指定を取得する
        baketype_color = context.scene.holomon_mrtk_channelmap_maker.prop_baketype_color

        # カスタムプロパティからメタリックベイクの実行指定を取得する
        baketype_metallic = context.scene.holomon_mrtk_channelmap_maker.prop_baketype_metallic

        # カスタムプロパティからオクルージョンベイクの実行指定を取得する
        baketype_occlusion = context.scene.holomon_mrtk_channelmap_maker.prop_baketype_occlusion

        # カスタムプロパティからエミッションベイクの実行指定を取得する
        baketype_emission = context.scene.holomon_mrtk_channelmap_maker.prop_baketype_emission

        # カスタムプロパティから滑らかさベイクの実行指定を取得する
        baketype_smoothness = context.scene.holomon_mrtk_channelmap_maker.prop_baketype_smoothness

        # カスタムプロパティから滑らかさベイクの実行指定を取得する
        baketype_normal = context.scene.holomon_mrtk_channelmap_maker.prop_baketype_normal


        # 少なくとも一つ以上ベイク対象が指定されているか確認する
        if not (baketype_color or baketype_metallic or baketype_occlusion
                or baketype_emission or baketype_smoothness or baketype_normal):
            # ベイク対象が指定されていない場合はエラーメッセージを表示する
            self.report({'ERROR'}, "Nothing : target bake map.")
            return {'CANCELLED'}


        # カスタムプロパティから指定中のオブジェクトを取得する
        target_object = context.scene.holomon_mrtk_channelmap_maker.prop_objectslect

        # 指定中のオブジェクトを確認する
        if target_object == None:
            # オブジェクトが指定されていない場合はエラーメッセージを表示する
            self.report({'ERROR'}, "Nothing : target object.")
            return {'CANCELLED'}

        # カスタムプロパティから指定中のテクスチャ名を取得する
        texture_name = context.scene.holomon_mrtk_channelmap_maker.prop_texturename

        # 指定中のテクスチャ名を確認する
        if texture_name == None:
            # テクスチャ名が指定されていない場合はエラーメッセージを表示する
            self.report({'ERROR'}, "Nothing : texture name.")
            return {'CANCELLED'}

        # カスタムプロパティから指定中のカラーテクスチャサイズを取得する
        colortexture_size = context.scene.holomon_mrtk_channelmap_maker.prop_colortexturesize

        # 指定中のカラーテクスチャサイズを確認する
        if colortexture_size < 1:
            # 適切なカラーテクスチャサイズが指定されていない場合はエラーメッセージを表示する
            self.report({'ERROR'}, "Nothing : color texture size.")
            return {'CANCELLED'}

        # カスタムプロパティから指定中のベイク余白を取得する
        bake_margin = context.scene.holomon_mrtk_channelmap_maker.prop_bakemargin

        # 指定中のテクスチャサイズを確認する
        if bake_margin < 0:
            # 適切なテクスチャサイズが指定されていない場合はエラーメッセージを表示する
            self.report({'ERROR'}, "Nothing : bake margin.")
            return {'CANCELLED'}


        # カスタムプロパティから指定中のチャンネルマップサイズを取得する
        channelmap_size = context.scene.holomon_mrtk_channelmap_maker.prop_channelmapsize

        # 指定中のチャンネルマップサイズを確認する
        if channelmap_size < 1:
            # 適切なチャンネルマップサイズが指定されていない場合はエラーメッセージを表示する
            self.report({'ERROR'}, "Nothing : channel map size.")
            return {'CANCELLED'}

        # カスタムプロパティから指定中のAO係数を取得する
        bake_aofactor = context.scene.holomon_mrtk_channelmap_maker.prop_aofactor

        # 指定中のAO係数を確認する
        if bake_aofactor < 0.0:
            # 適切なAO係数が指定されていない場合はエラーメッセージを表示する
            self.report({'ERROR'}, "Nothing : ao factor.")
            return {'CANCELLED'}

        # カスタムプロパティから指定中のAO距離を取得する
        bake_aodistance = context.scene.holomon_mrtk_channelmap_maker.prop_aodistance

        # 指定中のAO距離を確認する
        if bake_aodistance < 0.0:
            # 適切なAO距離が指定されていない場合はエラーメッセージを表示する
            self.report({'ERROR'}, "Nothing : ao distance.")
            return {'CANCELLED'}
        
        # カラーテクスチャとの比率に合わせてチャンネルマップ用のベイク余白を計算する
        channelmap_bakemargin = int(channelmap_size / int(colortexture_size / bake_margin))

        # カスタムプロパティから指定中のノーマルマップサイズを取得する
        normalmap_size = context.scene.holomon_mrtk_channelmap_maker.prop_normalmapsize

        # 指定中のノーマルマップサイズを確認する
        if normalmap_size < 1:
            # 適切なノーマルマップサイズが指定されていない場合はエラーメッセージを表示する
            self.report({'ERROR'}, "Nothing : normal map size.")
            return {'CANCELLED'}

        # カラーテクスチャとの比率に合わせてノーマルマップ用のベイク余白を計算する
        normalmap_bakemargin = int(normalmap_size / int(colortexture_size / bake_margin))


        # カスタムプロパティから新規スマートUV作成実行指定を取得する
        baketo_newsmartuv = context.scene.holomon_mrtk_channelmap_maker.prop_baketo_newsmartuv


        # UIの設定から各種実行ベイクの情報を作成する
        # カラーベイクの情報を作成する
        color_BakeProperties = UI_operations.BakeProperties(
            arg_execute_flg=baketype_color,
            arg_texture_name=texture_name + "_color",
            arg_texture_size=colortexture_size,
            arg_bake_margin=bake_margin
        )

        # メタリックベイクの情報を作成する
        metallic_BakeProperties = UI_operations.BakeProperties(
            arg_execute_flg=baketype_metallic,
            arg_texture_name=texture_name + "_metallic",
            arg_texture_size=channelmap_size,
            arg_bake_margin=channelmap_bakemargin
        )

        # 滑らかさベイクの情報を作成する
        smoothness_BakeProperties = UI_operations.BakeProperties(
            arg_execute_flg=baketype_smoothness,
            arg_texture_name=texture_name + "_smoothness",
            arg_texture_size=channelmap_size,
            arg_bake_margin=channelmap_bakemargin
        )

        # エミッションベイクの情報を作成する
        emission_BakeProperties = UI_operations.BakeProperties(
            arg_execute_flg=baketype_emission,
            arg_texture_name=texture_name + "_emission",
            arg_texture_size=channelmap_size,
            arg_bake_margin=channelmap_bakemargin
        )

        # オクルージョンベイクの情報を作成する
        occlusion_BakeProperties = UI_operations.AO_BakeProperties(
            arg_execute_flg=baketype_occlusion,
            arg_texture_name=texture_name + "_occlusion",
            arg_texture_size=channelmap_size,
            arg_bake_margin=channelmap_bakemargin,
            arg_ao_factor=bake_aofactor,
            arg_ao_distance=bake_aodistance
        )

        # ノーマルベイクの情報を作成する
        normal_BakeProperties = UI_operations.BakeProperties(
            arg_execute_flg=baketype_normal,
            arg_texture_name=texture_name + "_normal",
            arg_texture_size=normalmap_size,
            arg_bake_margin=normalmap_bakemargin
        )

        
        # チャネルマップ作成を実行する
        error_message = UI_operations.UI_mrtk_channelmap_maker(
            arg_target_object=target_object,
            arg_export_dir=self.directory,
            arg_export_filepath=self.filepath,
            arg_baketo_newsmartuv=baketo_newsmartuv,
            arg_colorbake_prop=color_BakeProperties,
            arg_metallicbake_prop=metallic_BakeProperties,
            arg_smoothnessbake_prop=smoothness_BakeProperties,
            arg_emissionbake_prop=emission_BakeProperties,
            arg_occlusionbake_prop=occlusion_BakeProperties,
            arg_normalbake_prop=normal_BakeProperties
        )
        
        # エラーメッセージの有無を確認する
        if error_message != None:
            # エラーメッセージが設定されている場合はエラーメッセージを表示する
            self.report({'ERROR'}, error_message)
            return {'CANCELLED'}

        return {'FINISHED'}


# PropertyGroupクラスの作成
# 参考URL:https://docs.blender.org/api/current/bpy.types.PropertyGroup.html
# マテリアル追加のプロパティ
class HOLOMON_addon_mrtk_material_maker_properties(PropertyGroup):
    # オブジェクト選択時のチェック関数を定義する
    def prop_object_select_poll(self, context, ):
        # メッシュオブジェクトのみ選択可能
        if(context and context.type in ('MESH', )):
            return True
        return False

    # シーン上のパネルに表示するオブジェクト選択用のカスタムプロパティを定義する
    prop_objectslect: PointerProperty(
        name = "Select Object",         # プロパティ名
        type = bpy.types.Object,        # タイプ
        description = "",               # 説明文
        poll = prop_object_select_poll, # チェック関数
    )
    # ※ アクティブオブジェクトを指定する仕様としたため
    #    オブジェクト選択のカスタムプロパティは利用しない

# マテリアルベイクのプロパティ
class HOLOMON_addon_mrtk_channelmap_maker_properties(PropertyGroup):
    # オブジェクト選択時のチェック関数を定義する
    def prop_object_select_poll(self, context, ):
        # メッシュオブジェクトのみ選択可能
        if(context and context.type in ('MESH', )):
            return True
        return False

    # ベイクタイプの更新時に実行する関数を定義する
    def change_baketype(self, context):
        print("change baketype")

    # シーン上のパネルに表示するオブジェクト選択用のカスタムプロパティを定義する
    prop_objectslect: PointerProperty(
        name = "Select Object",         # プロパティ名
        type = bpy.types.Object,        # タイプ
        description = "",               # 説明文
        poll = prop_object_select_poll, # チェック関数
    )


    # シーン上のパネルに表示するテクスチャ名指定用のカスタムプロパティを定義する
    prop_texturename: StringProperty(
        name="Texture Name",          # プロパティ名
        default="BakeTexture",        # デフォルト値
        maxlen=1024,                  # 最大文字列長
        description="",               # 説明文
    )

    # シーン上のパネルに表示するカラーテクスチャサイズ指定用のカスタムプロパティを定義する
    prop_colortexturesize: IntProperty(
        name = "Color Texture Size",  # プロパティ名
        default=2048,                 # デフォルト値
        description = "",             # 説明文
    )

    # シーン上のパネルに表示するノーマルマップサイズ指定用のカスタムプロパティを定義する
    prop_normalmapsize: IntProperty(
        name = "Normal Map Size",     # プロパティ名
        default=2048,                 # デフォルト値
        description = "",             # 説明文
    )

    # シーン上のパネルに表示するチャンネルマップサイズ指定用のカスタムプロパティを定義する
    prop_channelmapsize: IntProperty(
        name = "Channel Map Size",    # プロパティ名
        default=2048,                 # デフォルト値
        description = "",             # 説明文
    )

    # シーン上のパネルに表示するベイク余白用のカスタムプロパティを定義する
    prop_bakemargin: IntProperty(
        name = "Bake Margin",         # プロパティ名
        default=16,                   # デフォルト値
        description = "",             # 説明文
    )
    
    # シーン上のパネルに表示するAO係数用のカスタムプロパティを定義する
    prop_aofactor: FloatProperty(
        name = "Occlusion Factor",    # プロパティ名
        default=1.0,                  # デフォルト値
        description = "",             # 説明文
    )

    # シーン上のパネルに表示するAO距離用のカスタムプロパティを定義する
    prop_aodistance: FloatProperty(
        name = "Occlusion Distance",  # プロパティ名
        default=10.0,                 # デフォルト値
        description = "",             # 説明文
    )
    
    # シーン上のパネルに表示するカラーベイク実行用のカスタムプロパティを定義する
    prop_baketype_color: BoolProperty(
        name = "BakeType Color",      # プロパティ名
        default=True,                 # デフォルト値
        description = "",             # 説明文
        update=change_baketype,       # 更新時実行関数
    )
    
    # シーン上のパネルに表示するメタリックベイク実行用のカスタムプロパティを定義する
    prop_baketype_metallic: BoolProperty(
        name = "Bake Metallic Map",   # プロパティ名
        default=False,                # デフォルト値
        description = "",             # 説明文
        update=change_baketype,       # 更新時実行関数
    )
    
    # シーン上のパネルに表示するオクルージョンベイク実行用のカスタムプロパティを定義する
    prop_baketype_occlusion: BoolProperty(
        name = "Bake Occlusion Map",  # プロパティ名
        default=False,                # デフォルト値
        description = "",             # 説明文
        update=change_baketype,       # 更新時実行関数
    )
    
    # シーン上のパネルに表示するエミッションベイク実行用のカスタムプロパティを定義する
    prop_baketype_emission: BoolProperty(
        name = "Bake Emission Map",   # プロパティ名
        default=False,                # デフォルト値
        description = "",             # 説明文
        update=change_baketype,       # 更新時実行関数
    )
    
    # シーン上のパネルに表示する滑らかさベイク実行用のカスタムプロパティを定義する
    prop_baketype_smoothness: BoolProperty(
        name = "Bake Smoothness Map", # プロパティ名
        default=False,                # デフォルト値
        description = "",             # 説明文
        update=change_baketype,       # 更新時実行関数
    )
    
    # シーン上のパネルに表示するノーマルベイク実行用のカスタムプロパティを定義する
    prop_baketype_normal: BoolProperty(
        name = "Bake Normal Map",     # プロパティ名
        default=False,                # デフォルト値
        description = "",             # 説明文
        update=change_baketype,       # 更新時実行関数
    )
    
    # シーン上のパネルに表示する新規スマートUV作成実行用のカスタムプロパティを定義する
    prop_baketo_newsmartuv: BoolProperty(
        name = "Bake To New SmartUV", # プロパティ名
        default=False,                # デフォルト値
        description = "",             # 説明文
    )
    


# 登録に関する処理
# 登録対象のクラス名
regist_classes = (
    HOLOMON_PT_addon_mrtk_material_maker,
    HOLOMON_OT_addon_mrtk_material_maker,
    HOLOMON_addon_mrtk_material_maker_properties,
    HOLOMON_PT_addon_mrtk_channelmap_maker,
    HOLOMON_PT_addon_mrtk_channelmap_maker_option,
    HOLOMON_OT_addon_mrtk_channelmap_maker,
    HOLOMON_addon_mrtk_channelmap_maker_properties,
)

# 作成クラスと定義の登録メソッド
def register():
    # カスタムクラスを登録する
    for regist_cls in regist_classes:
        bpy.utils.register_class(regist_cls)
    # シーン情報にカスタムプロパティを登録する
    bpy.types.Scene.holomon_mrtk_material_maker = PointerProperty(type=HOLOMON_addon_mrtk_material_maker_properties)
    bpy.types.Scene.holomon_mrtk_channelmap_maker = PointerProperty(type=HOLOMON_addon_mrtk_channelmap_maker_properties)

# 作成クラスと定義の登録解除メソッド
def unregister():
    # シーン情報のカスタムプロパティを削除する
    del bpy.types.Scene.holomon_mrtk_material_maker
    del bpy.types.Scene.holomon_mrtk_channelmap_maker
    # カスタムクラスを解除する
    for regist_cls in regist_classes:
        bpy.utils.unregister_class(regist_cls)



# 実行時の処理
if __name__ == "__main__":
    # 作成クラスと定義を登録する
    register()


