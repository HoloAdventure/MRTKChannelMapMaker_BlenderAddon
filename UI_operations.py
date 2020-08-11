# 各種ライブラリインポート
if "bpy" in locals():
    import importlib
    if "add_material_MRTKmaterial" in locals():
        importlib.reload(add_material_MRTKmaterial)
    if "bake_materialcolor_texture" in locals():
        importlib.reload(bake_materialcolor_texture)
    if "bake_metallic_texture" in locals():
        importlib.reload(bake_metallic_texture)
    if "bake_ambientocclusion_texture" in locals():
        importlib.reload(bake_ambientocclusion_texture)
    if "bake_whiteemission_texture" in locals():
        importlib.reload(bake_whiteemission_texture)
    if "bake_smoothness_texture" in locals():
        importlib.reload(bake_smoothness_texture)
    if "bake_materialnormal_texture" in locals():
        importlib.reload(bake_materialnormal_texture)
    if "control_uvlayer" in locals():
        importlib.reload(control_uvlayer)
    if "save_replace_datas" in locals():
        importlib.reload(save_replace_datas)
    if "accessor_control_MRTKstandard" in locals():
        importlib.reload(accessor_control_MRTKstandard)
import bpy
from . import add_material_MRTKmaterial
from . import bake_materialcolor_texture
from . import bake_metallic_texture
from . import bake_ambientocclusion_texture
from . import bake_whiteemission_texture
from . import bake_smoothness_texture
from . import bake_materialnormal_texture
from . import control_uvlayer
from . import save_replace_datas
from . import accessor_control_MRTKstandard

# ベイク実行時の定型情報
class BakeProperties:
    # コンストラクタの定義
    def __init__(
      self,
      arg_execute_flg:bool=False,
      arg_texture_name:str="",
      arg_texture_size:int=0,
      arg_bake_margin:int=0
      ):
        """コンストラクタ

        Args:
            arg_execute_flg (bool, optional): ベイク実行フラグ. Defaults to False.
            arg_texture_name (str, optional): テクスチャ名. Defaults to "".
            arg_texture_size (int, optional): テクスチャサイズ. Defaults to 0.
            arg_bake_margin (int, optional): ベイク余白(px). Defaults to 0.
        """
        self.execute_flg=arg_execute_flg     # ベイク実行フラグ
        self.texture_name=arg_texture_name   # テクスチャ名
        self.texture_size=arg_texture_size   # テクスチャサイズ
        self.bake_margin=arg_bake_margin     # ベイク余白(px)

# AOベイク実行時の拡張情報
class AO_BakeProperties(BakeProperties):
    # コンストラクタの定義
    def __init__(
      self,
      arg_execute_flg:bool=False,
      arg_texture_name:str="",
      arg_texture_size:int=0,
      arg_bake_margin:int=0,
      arg_ao_factor:float=0.0,
      arg_ao_distance:float=0.0,
      ):
        """コンストラクタ

        Args:
            arg_execute_flg (bool, optional): ベイク実行フラグ. Defaults to False.
            arg_texture_name (str, optional): テクスチャ名. Defaults to "".
            arg_texture_size (int, optional): テクスチャサイズ. Defaults to 0.
            arg_bake_margin (int, optional): ベイク余白(px). Defaults to 0.
            arg_ao_factor (float, optional): AO係数. Defaults to 0.0.
            arg_ao_distance (float, optional): AO距離. Defaults to 0.0.
        """
        super(AO_BakeProperties, self).__init__(
            arg_execute_flg=arg_execute_flg,
            arg_texture_name=arg_texture_name,
            arg_texture_size=arg_texture_size,
            arg_bake_margin=arg_bake_margin
        )
        self.ao_factor=arg_ao_factor     # AO係数
        self.ao_distance=arg_ao_distance # AO距離



# マテリアル作成ボタンの処理を実行する
def UI_mrtk_material_maker(arg_object:bpy.types.Object, arg_materialname:str) -> str:
    """マテリアル作成ボタンの処理を実行する

    Args:
        arg_object (bpy.types.Object): 指定オブジェクト
        arg_materialname (str): 作成マテリアル名

    Returns:
        str: エラーメッセージ(正常時 None)
    """
    
    # マテリアルを追加する
    add_result = add_material_MRTKmaterial.add_materialslot_nodegroupmaterial(
        arg_object=arg_object,
        arg_materialname=arg_materialname
    )
    
    # 実行結果を確認する
    if add_result == False:
        # 実行に失敗していた場合はエラーメッセージを返す
        return "Method : Failed to add material."

    # 正常終了時は None を返す
    return None


# チャネルマップ作成実行ボタンの処理を実行する
def UI_mrtk_channelmap_maker(
  arg_tobake_object:bpy.types.Object,
  arg_export_dir:str,
  arg_export_filepath:str,
  arg_colorbake_prop:BakeProperties,
  arg_metallicbake_prop:BakeProperties,
  arg_smoothnessbake_prop:BakeProperties,
  arg_emissionbake_prop:BakeProperties,
  arg_occlusionbake_prop:AO_BakeProperties,
  arg_normalbake_prop:BakeProperties,
  ) -> str:
    """[summary]

    Returns:
        str: エラーメッセージ(正常時 None)
    """

    # 対象のオブジェクトのマテリアルが全てMRTKStandardノードグループを使用したマテリアルかチェックする
    all_MRTKstandard = accessor_control_MRTKstandard.check_object_materials(arg_object=arg_tobake_object)

    # マテリアルが全てMRTKStandardノードグループか確認する
    if all_MRTKstandard == False:
        # マテリアルが全てMRTKStandardノードグループに設定されていない場合はエラーメッセージを表示する
        return "Object : All materials must be MRTK Standard."

    # アクティブなUVマップレイヤーが存在するか確認する
    # 存在しない場合は作成する
    active_uvlayer = control_uvlayer.get_uvlayer(arg_object=arg_tobake_object)
    # UVマップレイヤーの取得、作成に失敗したか確認する
    if active_uvlayer == None:
        # UVマップレイヤーの取得、作成に失敗した場合はエラーメッセージを表示する
        return "Object : missing UVmap."


    # 作成した各テクスチャの参照を保持する
    colorbake_image = None
    metallicbake_image = None
    smoothnessbake_image = None
    emissionbake_image = None
    occlusionbake_image = None
    normalbake_image = None


    # カラーベイクを実行する
    if arg_colorbake_prop.execute_flg == True:
        # 指定オブジェクトの全てのマテリアルカラーを画像テクスチャにベイクする
        colorbake_image = bake_materialcolor_texture.bake_materialcolor_texture(
            arg_object=arg_tobake_object,
            arg_texturename=arg_colorbake_prop.texture_name,
            arg_texturesize=arg_colorbake_prop.texture_size,
            arg_bakemargin=arg_colorbake_prop.bake_margin
        )

        # 指定ディレクトリに作成した画像ファイルを出力する
        save_replace_datas.save_image_targetdir(
            arg_image=colorbake_image,
            arg_directory=arg_export_dir
        )


    # メタリックベイクを実行する
    if arg_metallicbake_prop.execute_flg == True:
        # 指定オブジェクトのメタリックを画像テクスチャにベイクする
        metallicbake_image = bake_metallic_texture.bake_metallic_texture(
            arg_object=arg_tobake_object,
            arg_texturename=arg_metallicbake_prop.texture_name,
            arg_texturesize=arg_metallicbake_prop.texture_size,
            arg_bakemargin=arg_metallicbake_prop.bake_margin
        )

        # 指定ディレクトリに作成した画像ファイルを出力する
        save_replace_datas.save_image_targetdir(
            arg_image=metallicbake_image,
            arg_directory=arg_export_dir
        )


    # 滑らかさベイクを実行する
    if arg_smoothnessbake_prop.execute_flg == True:
        # 指定オブジェクトの滑らかさを画像テクスチャにベイクする
        smoothnessbake_image = bake_smoothness_texture.bake_smoothness_texture(
            arg_object=arg_tobake_object,
            arg_texturename=arg_smoothnessbake_prop.texture_name,
            arg_texturesize=arg_smoothnessbake_prop.texture_size,
            arg_bakemargin=arg_smoothnessbake_prop.bake_margin
        )

        # 指定ディレクトリに作成した画像ファイルを出力する
        save_replace_datas.save_image_targetdir(
            arg_image=smoothnessbake_image,
            arg_directory=arg_export_dir
        )


    # エミッションベイクを実行する
    if arg_emissionbake_prop.execute_flg == True:
        # 指定オブジェクトのエミッションを画像テクスチャにベイクする
        emissionbake_image = bake_whiteemission_texture.bake_whiteemission_texture(
            arg_object=arg_tobake_object,
            arg_texturename=arg_emissionbake_prop.texture_name,
            arg_texturesize=arg_emissionbake_prop.texture_size,
            arg_bakemargin=arg_emissionbake_prop.bake_margin
        )

        # 指定ディレクトリに作成した画像ファイルを出力する
        save_replace_datas.save_image_targetdir(
            arg_image=emissionbake_image,
            arg_directory=arg_export_dir
        )


    # オクルージョンベイクを実行する
    if arg_occlusionbake_prop.execute_flg == True:
        # 指定オブジェクトのアンビエントオクルージョンを画像テクスチャにベイクする
        occlusionbake_image = bake_ambientocclusion_texture.bake_ambientocclusion_texture(
            arg_object=arg_tobake_object,
            arg_texturename=arg_occlusionbake_prop.texture_name,
            arg_texturesize=arg_occlusionbake_prop.texture_size,
            arg_bakemargin=arg_occlusionbake_prop.bake_margin,
            arg_aofactor=arg_occlusionbake_prop.ao_factor,
            arg_distance=arg_occlusionbake_prop.ao_distance
        )

        # 指定ディレクトリに作成した画像ファイルを出力する
        save_replace_datas.save_image_targetdir(
            arg_image=occlusionbake_image,
            arg_directory=arg_export_dir
        )


    # ノーマルベイクを実行する
    if arg_normalbake_prop.execute_flg:
        # 指定オブジェクトのノーマルマップを画像テクスチャにベイクする
        normalbake_image = bake_materialnormal_texture.bake_materialnormal_texture(
            arg_object=arg_tobake_object,
            arg_texturename=arg_normalbake_prop.texture_name,
            arg_texturesize=arg_normalbake_prop.texture_size,
            arg_bakemargin=arg_normalbake_prop.bake_margin
        )

        # 指定ディレクトリに作成した画像ファイルを出力する(16ビット色深度)
        save_replace_datas.save_image_targetdir(
            arg_image=normalbake_image,
            arg_directory=arg_export_dir,
            arg_colormode='RGBA',
            arg_colordepth='16',
            arg_compression=15
        )


    # カラーベイクの後処理を実行する
    if arg_colorbake_prop.execute_flg == True:
        # 指定オブジェクトのマテリアルを作成テクスチャのシンプルなプリンシプルBSDFマテリアルのみとする
        save_replace_datas.replace_material_textureBSDF(
            arg_object=arg_tobake_object,
            arg_texture=colorbake_image
        )


    # 画像の参照と統一マテリアルを生成したプロジェクトを別名ファイルとして保存する
    bpy.ops.wm.save_as_mainfile(filepath=arg_export_filepath)

    # 正常終了時は None を返す
    return None


