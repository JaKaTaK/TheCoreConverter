##################################################
#
# Filename: TheCoreRemapper.py
# Author: Jonny Weiss
# Description: Script to take the LM layouts of TheCore and generate the other 44 layouts.
# Change Log:
#   9/25/12 - Created
#   9/26/12 - Finished initial functionality
#
##################################################
from configparser import SafeConfigParser
import os, sys

TRANSLATE = not "US" in sys.argv
ONLY_SEED = "LM" in sys.argv

GLOBAL = -1
LMM = 0
RMM = 1
RM = 2

SHOW_HOTS_MISSING = True
SHOW_DUPLICATES = False
VERIFY_ALL = False

CAMERA_KEYS = ['CameraSave0', 'CameraSave1', 'CameraSave2', 'CameraSave3', 'CameraSave4', 'CameraSave5', 'CameraSave6', 'CameraSave7',
               'CameraView0', 'CameraView1', 'CameraView2', 'CameraView3', 'CameraView4', 'CameraView5', 'CameraView6', 'CameraView7']

# ZERG_CONTROL_GROUP_SPECIAL = ['ControlGroupAssign7']

CONTROL_GROUP_KEYS = ['ControlGroupAppend0', 'ControlGroupAppend1', 'ControlGroupAppend2', 'ControlGroupAppend3', 'ControlGroupAppend4', 'ControlGroupAppend5', 'ControlGroupAppend6', 'ControlGroupAppend7', 'ControlGroupAppend8', 'ControlGroupAppend9',
                      'ControlGroupAssign0', 'ControlGroupAssign1', 'ControlGroupAssign2', 'ControlGroupAssign3', 'ControlGroupAssign4', 'ControlGroupAssign5', 'ControlGroupAssign6', 'ControlGroupAssign7', 'ControlGroupAssign8', 'ControlGroupAssign9',
                      'ControlGroupRecall0', 'ControlGroupRecall1', 'ControlGroupRecall2', 'ControlGroupRecall3', 'ControlGroupRecall4', 'ControlGroupRecall5', 'ControlGroupRecall6', 'ControlGroupRecall7', 'ControlGroupRecall8', 'ControlGroupRecall9',
                      'ControlGroupAppendAndSteal0', 'ControlGroupAppendAndSteal1', 'ControlGroupAppendAndSteal2', 'ControlGroupAppendAndSteal3', 'ControlGroupAppendAndSteal4', 'ControlGroupAppendAndSteal5', 'ControlGroupAppendAndSteal6', 'ControlGroupAppendAndSteal7', 'ControlGroupAppendAndSteal8', 'ControlGroupAppendAndSteal9',
                      'ControlGroupAssignAndSteal0', 'ControlGroupAssignAndSteal1', 'ControlGroupAssignAndSteal2', 'ControlGroupAssignAndSteal3', 'ControlGroupAssignAndSteal4', 'ControlGroupAssignAndSteal5', 'ControlGroupAssignAndSteal6', 'ControlGroupAssignAndSteal7', 'ControlGroupAssignAndSteal8', 'ControlGroupAssignAndSteal9', ]


# Add to this please.
GENERAL_KEYS = ['FPS', 'Music', 'Sound', 'PTT', 'DialogDismiss', 'MenuAchievements', 'MenuGame', 'MenuMessages', 'MenuSocial',
                'LeaderResources', 'LeaderIncome', 'LeaderSpending', 'LeaderUnits', 'LeaderUnitsLost', 'LeaderProduction', 'LeaderArmy',
                'LeaderAPM', 'LeaderCPM', 'ObserveAllPlayers', 'ObserveAutoCamera', 'ObserveClearSelection', 'ObservePlayer0', 'ObservePlayer1',
                'ObservePlayer2', 'ObservePlayer3', 'ObservePlayer4', 'ObservePlayer5', 'ObservePlayer6', 'ObservePlayer7', 'ObservePlayer8',
                'ObservePlayer9', 'ObservePlayer10', 'ObservePlayer11', 'ObservePlayer12', 'ObservePlayer13', 'ObservePlayer14', 'ObservePlayer15',
                'ObserveSelected', 'ObservePreview', 'ObserveStatusBars', 'StatPanelResources', 'StatPanelArmySupply', 'StatPanelUnitsLost', 'StatPanelAPM', 'StatPanelCPM',
                'ToggleWorldPanel', 'CinematicSkip', 'AlertRecall', 'CameraFollow', 'GameTooltipsOn', 'IdleWorker', 'MinimapColors', 'MinimapPing',
                'MinimapTerrain', 'PauseGame', 'QuickPing', 'QuickSave', 'ReplayPlayPause', 'ReplayRestart', 'ReplaySkipBack', 'ReplaySkipNext', 'ReplaySpeedDec',
                'ReplaySpeedInc', 'ReplayStop', 'ReplayHide', 'SelectionCancelDrag', 'SubgroupNext', 'SubgroupPrev', 'TeamResources', 'TownCamera', 'WarpIn',
                'Cancel', 'CancelCocoon', 'CancelMutateMorph', 'CancelUpgradeMorph', 'ChatCancel',
                'ChatAll', 'ChatDefault', 'ChatIndividual', 'ChatRecipient', 'ChatAllies',
                'CameraTurnLeft', 'CameraTurnRight', 'CameraCenter',
                'StatusAll', 'StatusOwner', 'StatusEnemy', 'StatusAlly', 'MenuHelp', 'NamePanel', 'ArmySelect', 'SelectBuilder', 'ToggleVersusModeSides']

EXCLUDE_MAPPING = ['AllowSetConflicts']

SAME_CHECKS = [['Pylon/Probe', 'SupplyDepot/SCV', 'SupplyDepotDrop/SCV'],
               ['Assimilator/Probe', 'Extractor/Drone', 'Refinery/SCV', 'AutomatedRefinery/SCV', 'AutomatedExtractor/Drone'],
               ['Gateway/Probe', 'Barracks/SCV'],
               ['Nexus/Probe', 'Hatchery/Drone', 'CommandCenter/SCV', 'CommandCenterOrbRelay/SCV'],
               ['Forge/Probe', 'EvolutionChamber/Drone', 'EngineeringBay/SCV'],
               ['RoboticsFacility/Probe', 'Factory/SCV'],
               ['Stargate/Probe', 'Spire/Drone', 'Starport/SCV'],
               ['TwilightCouncil/Probe', 'Armory/SCV'],
               ['FleetBeacon/Probe', 'FusionCore/SCV'],
               ['ProtossGroundWeaponsLevel1/Forge', 'TerranInfantryWeaponsLevel1/EngineeringBay', 'TerranInfantryWeaponsUltraCapacitorsLevel1/EngineeringBay', 'TerranInfantryWeaponsUltraCapacitorsLevel2/EngineeringBay', 'TerranInfantryWeaponsUltraCapacitorsLevel3/EngineeringBay'],
               ['ProtossGroundArmorLevel1/Forge', 'TerranInfantryArmorLevel1/EngineeringBay', 'zerggroundarmor1/EvolutionChamber', 'TerranInfantryArmorVanadiumPlatingLevel1/EngineeringBay', 'TerranInfantryArmorVanadiumPlatingLevel2/EngineeringBay', 'TerranInfantryArmorVanadiumPlatingLevel3/EngineeringBay'],
               ['ProtossAirWeaponsLevel1/CyberneticsCore', 'TerranShipWeaponsLevel1/Armory', 'zergflyerattack1'],
               ['TerranShipWeaponsLevel1/Armory', 'TerranShipWeaponsUltraCapacitorsLevel1/Armory', 'TerranShipWeaponsUltraCapacitorsLevel2/Armory', 'TerranShipWeaponsUltraCapacitorsLevel3/Armory'],
               ['ProtossAirArmorLevel1/CyberneticsCore', 'TerranShipPlatingLevel1/Armory', 'zergflyerarmor1'],
               ['TerranShipPlatingLevel1/Armory', 'TerranShipPlatingVanadiumPlatingLevel1/Armory', 'TerranShipPlatingVanadiumPlatingLevel2/Armory', 'TerranShipPlatingVanadiumPlatingLevel3/Armory'],
               ['Stim', 'StimFirebat/Firebat', 'StimFirebat/DevilDog'],
               ['Heal/Medivac', 'BonesHeal/Stetmann', 'NanoRepair/ScienceVessel', 'MedicHeal/Medic', 'MercMedicHeal/MercMedic'],
               ['CloakOnBanshee', 'RogueGhostCloak/Spectre', 'WraithCloakOn/Wraith'],
               ['CloakOff', 'WraithCloakOff/Wraith'],
#               ['WeaponsFree/Ghost','SpectreWeaponsFree/Spectre'], thanks to HotS Spectre key now unbinds if set to same as HoldFire, Ghost HoldFire & weapons free toggle works correctly
               ['GhostHoldFire/Ghost', 'SpectreHoldFire/Spectre'],
               ['NukeArm/GhostAcademy', 'SpectreNukeArm/GhostAcademy'],
               ['NukeCalldown/Ghost', 'SpectreNukeCalldown/Spectre', 'HeroNukeCalldown/Nova', 'HeroNukeCalldown/Tosh', 'OdinNukeCalldown/Odin'],
               ['BunkerLoad', 'HerculesLoad/Hercules'],
               ['BunkerUnloadAll', 'HerculesUnloadAll/Hercules'],
               ['Reactor/Barracks', 'Reactor/BarracksFlying', 'Reactor/Factory', 'Reactor/FactoryFlying', 'Reactor/Starport', 'Reactor/StarportFlying'],
               ['TechLabBarracks/Barracks', 'TechLabBarracks/BarracksFlying', 'TechReactor/Barracks', 'TechReactor/BarracksFlying', 'TechLabFactory/Factory', 'BuildTechLabFactory/FactoryFlying', 'TechReactor/Factory', 'TechReactor/FactoryFlying', 'TechLabStarport/Starport', 'BuildTechLabStarport/StarportFlying', 'TechReactor/Starport', 'TechReactor/StarportFlying'],
#               ['Ghost/Barracks','Spectre/Barracks'], thanks to HotS campaign these can no longer be on the same key
               ['Raven/Starport', 'BuildScienceVessel/Starport'],
               ['EMP/Ghost', 'UltrasonicPulse/Spectre'],
               ['Snipe/Ghost', 'NovaSnipe/Nova', 'Obliterate/Spectre'],
               ['Lair/Hatchery', 'Hive/Lair', 'LurkerDen/HydraliskDen', 'ImpalerDen/HydraliskDen'],
               ['MassRecall/Mothership', 'MassRecall/Artanis', 'MothershipMassRecall/Mothership', 'MothershipCoreMassRecall/MothershipCore'],
               ['Vortex/Mothership', 'Vortex/Artanis'],
               ['Mothership/Nexus', 'MothershipCore/Nexus'],
               ['AutoTurret/Raven', 'BuildAutoTurret/Raven'],
               ['PointDefenseDrone/Raven', 'BuildPointDefenseDrone/Raven'],
               ['ResearchShieldWall/BarracksTechLab', 'ResearchShieldWall/BarracksTechReactor'],
               ['Stimpack/BarracksTechLab', 'Stimpack/BarracksTechReactor'],
               ['ResearchPunisherGrenades/BarracksTechLab', 'ResearchPunisherGrenades/BarracksTechReactor', 'ResearchJackhammerConcussionGrenade/BarracksTechLab', 'ResearchJackhammerConcussionGrenade/BarracksTechReactor'],
               ['ReaperSpeed/BarracksTechLab', 'ReaperSpeed/BarracksTechReactor', 'ResearchG4Charge/BarracksTechLab', 'ResearchG4Charge/BarracksTechReactor'],
               ['ResearchIncineratorNozzles/BarracksTechLab', 'ResearchIncineratorNozzles/BarracksTechReactor'],
               ['ResearchStabilizerMedPacks/BarracksTechLab', 'ResearchStabilizerMedPacks/BarracksTechReactor'],
               ['ResearchCerberusMines/FactoryTechLab', 'ResearchCerberusMines/FactoryTechReactor'],
               ['ResearchHighCapacityBarrels/FactoryTechLab', 'ResearchHighCapacityBarrels/FactoryTechReactor'],
               ['ResearchMultiLockTargetingSystem/FactoryTechLab', 'ResearchMultiLockTargetingSystem/FactoryTechReactor'],
               ['ResearchRegenerativeBioSteel/FactoryTechLab', 'ResearchRegenerativeBioSteel/FactoryTechReactor'],
               ['ResearchStrikeCannons/FactoryTechLab', 'ResearchStrikeCannons/FactoryTechReactor'],
               ['ResearchSiegeTech/FactoryTechLab', 'ResearchSiegeTech/FactoryTechReactor', 'ResearchShapedBlast/FactoryTechLab', 'ResearchShapedBlast/FactoryTechReactor'],
               ['ResearchMedivacEnergyUpgrade/StarportTechLab', 'ResearchMedivacEnergyUpgrade/StarportTechReactor'],
               ['ResearchBansheeCloak/StarportTechLab', 'ResearchBansheeCloak/StarportTechReactor'],
               ['ResearchDurableMaterials/StarportTechLab', 'ResearchDurableMaterials/StarportTechReactor'],
               ['ResearchSeekerMissile/StarportTechLab', 'ResearchSeekerMissile/StarportTechReactor'],
               ['ResearchRavenEnergyUpgrade/StarportTechLab', 'ResearchRavenEnergyUpgrade/StarportTechReactor'],
               ['WraithCloak/StarportTechLab', 'WraithCloak/StarportTechReactor'],
               ['Baneling/Zergling', 'Baneling/Zergling2', 'Baneling/HotSRaptor', 'Baneling/HotSSwarmling', 'MorphtoHunter/HotSRaptor', 'MorphtoHunter/HotSSwarmling', 'MorphtoSplitterling/HotSRaptor', 'MorphtoSplitterling/HotSSwarmling'],
               ['DisableBuildingAttack/Baneling', 'DisableBuildingAttack/baneling', 'DisableBuildingAttack/baneling2', 'DisableBuildingAttack/HotSHunter', 'DisableBuildingAttack/HotSSplitterlingBig'],
               ['EnableBuildingAttack/Baneling', 'EnableBuildingAttack/baneling', 'EnableBuildingAttack/baneling2', 'EnableBuildingAttack/HotSHunter', 'EnableBuildingAttack/HotSSplitterlingBig'],
               ['Explode/Baneling', 'Explode/BanelingBurrowed', 'Explode/baneling', 'Explode/baneling2', 'Explode/HotSSplitterlingBig', 'Explode/HotSSplitterlingBigBurrowed', 'Explode/HotSHunter', 'Explode/HotSHunterBurrowed'],
               ['ForceField/Sentry', 'ForceField2/Sentry2'],
               ['FungalGrowth/Infestor', 'FungalGrowth/Infestor2'],
               ['GuardianShield/Sentry', 'GuardianShield/Sentry2'],
               ['Hallucination/Sentry', 'Hallucination/Sentry2'],
               ['Heal/Medivac', 'Heal/Medivac2'],
               ['InfestedTerrans/Infestor', 'InfestedTerrans/Infestor2'],
               ['NeuralParasite/Infestor', 'NeuralParasite/Infestor2', 'NPSwarm/Infestor'],
               ['Baneling/Zergling', 'Baneling/Zergling2', 'Baneling/HotSRaptor', 'Baneling/HotSSwarmling'],
               ['Apocalypse/K5Kerrigan', 'K5DropPods/K5Kerrigan', 'K5Leviathan/K5Kerrigan'],
               ['MindBolt/K5Kerrigan', 'MindBolt/KerriganGhostLab', 'PrimalSlash/K5Kerrigan'],
               ['PrimalHeal/K5Kerrigan', 'SpawnBanelings/K5Kerrigan', 'WildMutation/K5Kerrigan'],
               ['PsiStrike/K5Kerrigan', 'PsionicLift/K5Kerrigan', 'PsionicLift/KerriganGhostLab'],
               ['YamatoGun', 'SJHyperionYamato/SJHyperion','HyperionVoidCoopYamatoCannon/HyperionVoidCoop'],
               ['Hydralisk/Larva', 'MorphToHydraliskImpaler/Larva', 'MorphToHydraliskLurker/Larva'],
               ['Infestor/Larva', 'MorphtoDefiler/Larva'],
               ['Mutalisk/Larva', 'MorphToMutaliskBroodlord/Larva', 'MorphToMutaliskViper/Larva'],
               ['Roach/Larva', 'MorphToVile/Larva', 'MorphToCorpser/Larva'],
               ['SwarmHostMP/Larva', 'MorphToSwarmHostSplitA/Larva', 'MorphToSwarmHostSplitB/Larva'],
               ['Ultralisk/Larva', 'MorphToHotSNoxious/Larva', 'MorphToHotSTorrasque/Larva'],
               ['Viper/Larva', 'Aberration/Larva'],
               ['Zergling/Larva', 'MorphToSwarmling/Larva', 'MorphToRaptor/Larva'],
               ['LocustLaunch/SwarmHostBurrowed', 'LocustFlyingLaunch/SwarmHostSplitABurrowed', 'LocustFlyingLaunch/SwarmHostSplitARooted', 'LocustLaunch/SwarmHostRooted', 'LocustLaunchCreeper/SwarmHostSplitBBurrowed', 'LocustLaunchCreeper/SwarmHostSplitBRooted'],
               ['BurrowDown', 'BurrowHydraliskImpalerDown', 'BurrowHydraliskLurkerDown', 'ImpalerBurrowDown', 'LurkerBurrowDown'],
               ['BurrowUp', 'BurrowHydraliskImpalerUp', 'BurrowHydraliskLurkerUp', 'ImpalerBurrowUp', 'LurkerBurrowUp'],  # 'SwarmHostUprootUnburrow/SwarmHostBurrowed','SwarmHostUprootUnburrow/SwarmHostSplitABurrowed','SwarmHostUprootUnburrow/SwarmHostSplitBBurrowed'
               ['SwarmHostDeepBurrow/SwarmHostSplitB', 'SwarmHostDeepBurrow/SwarmHostSplitBBurrowed', 'SwarmHostDeepBurrow/SwarmHostSplitBRooted'],
               ['SwarmHostRoot/SwarmHost', 'SwarmHostRoot/SwarmHostSplitA', 'SwarmHostRoot/SwarmHostSplitB'],
               ['SwarmHostUproot/SwarmHostRooted', 'SwarmHostUproot/SwarmHostSplitARooted', 'SwarmHostUproot/SwarmHostSplitBRooted'],
               ['HydraliskFrenzy/Hydralisk', 'HydraliskFrenzy/HydraliskImpaler', 'HydraliskFrenzy/HydraliskLurker'],
               ['Impaler/HydraliskImpaler', 'Lurker/HydraliskLurker'],
               ['BroodLord/Corruptor', 'BroodLord/MutaliskBroodlord', 'Viper/MutaliskViper'],
               ['BlindingCloud/Viper', 'DisablingCloud/Viper'],
               ['ViperConsume/Viper', 'ViperConsumption/Viper'],
               ['BurrowChargeMP/Ultralisk', 'BurrowChargeCampaign/Ultralisk', 'BurrowChargeCampaign/HotSTorrasque', 'BurrowChargeCampaignNoxious/HotSNoxious'],
               ['Transfusion/Queen', 'Transfusion/Queen2', 'QueenBurstHeal/Queen'],
               ['GrowHugeQueen/LargeSwarmQueen', 'GrowLargeQueen/SwarmQueen', 'GrowSwarmQueen/LarvalQueen'],
               ['SwarmQueenHydralisk/HugeSwarmQueen', 'SwarmQueenHydralisk/SwarmQueenEgg', 'SwarmQueenHydraliskImpaler/HugeSwarmQueen', 'SwarmQueenHydraliskImpaler/LargeSwarmQueen', 'SwarmQueenHydraliskImpaler/SwarmQueen', 'SwarmQueenHydraliskLurker/HugeSwarmQueen', 'SwarmQueenHydraliskLurker/LargeSwarmQueen', 'SwarmQueenHydraliskLurker/SwarmQueen'],
               ['ParasiticInvasion/LarvalQueen', 'SwarmQueenParasiticInvasion/HugeSwarmQueen', 'SwarmQueenParasiticInvasion/LargeSwarmQueen', 'SwarmQueenParasiticInvasion/SwarmQueen'],
               ['SwarmQueenCorpser/LargeSwarmQueen', 'SwarmQueenCorpser/HugeSwarmQueen', 'SwarmQueenCorpser/SwarmQueen', 'SwarmQueenRoach/HugeSwarmQueen', 'SwarmQueenRoach/LargeSwarmQueen', 'SwarmQueenRoach/SwarmQueenEgg', 'SwarmQueenVile/HugeSwarmQueen', 'SwarmQueenVile/LargeSwarmQueen', 'SwarmQueenVile/SwarmQueen'],
               ['SwarmQueenRaptor/HugeSwarmQueen', 'SwarmQueenRaptor/LargeSwarmQueen', 'SwarmQueenRaptor/SwarmQueen', 'SwarmQueenSwarmling/HugeSwarmQueen', 'SwarmQueenSwarmling/LargeSwarmQueen', 'SwarmQueenSwarmling/SwarmQueen', 'SwarmQueenZergling/HugeSwarmQueen', 'SwarmQueenZergling/LargeSwarmQueen', 'SwarmQueenZergling/SwarmQueen', 'SwarmQueenZergling/SwarmQueenEgg'],
               ['GreaterSpire/Spire', 'GreaterSpireBroodlord/Spire'],
               ['RespawnZergling/Hatchery', 'RespawnZergling/Hive', 'RespawnZergling/Lair'],
               # ['GenerateCreep/Overlord','StopGenerateCreep/Overlord']]
               ['VoidSentryShieldRepair/Sentry','VoidSentryShieldRepairDouble/SentryAiur'],
               ['UpgradeToWarpGate/Gateway','UpgradeToRoboticsFacilityWarp/RoboticsFacility','UpgradeToStargateWarp/Stargate'],
               ['MorphBackToGateway/WarpGate','MorphBackToRoboticsFacility/RoboticsFacilityWarp',],
               ['Vortex/Mothership','Vortex/Artanis','VoidSentryBlackHole/SOAMothershipv4','TemporalField/Mothership','TemporalField/MothershipCore'],
               ['250mmStrikeCannons/Thor','250mmStrikeCannons/ThorWreckageSwann'],
               ['SelfRepair/Thor','SelfRepair/ThorWreckageSwann'],
               ['Salvage/Bunker','Salvage/MissileTurret','Salvage/KelMorianGrenadeTurret','Salvage/PerditionTurret','Salvage/KelMorianMissileTurret'],
               ['Hyperjump/Battlecruiser','HyperionVoidCoopHyperjump/HyperionVoidCoop','HyperjumpHercules/Hercules'],
               ['Charge/Zealot','Charge/ZealotAiur','Charge/ZealotPurifier','VoidZealotShadowCharge/ZealotShakuras','Charge/ShadowOfTheVoidZealot'],
               ['ResearchIncineratorGauntlets/BarracksTechLab','ResearchIncineratorGauntlets/BarracksTechReactor'],
               ['ResearchJuggernautPlating/BarracksTechLab','ResearchJuggernautPlating/BarracksTechReactor'],['ResearchStabilizerMedpacks/BarracksTechLab','ResearchStabilizerMedpacks/BarracksTechReactor'],
               ['ResearchHellbatHellArmor/FactoryTechLab','ResearchHellbatHellArmor/FactoryTechReactor'],
               ['ResearchAresClassTargetingSystem/FactoryTechLab','ResearchAresClassTargetingSystem/FactoryTechReactor'],
               ['ResearchMultiLockWeaponsSystem/FactoryTechLab','ResearchMultiLockWeaponsSystem/FactoryTechReactor'],
               ['ResearchMaelstromRounds/FactoryTechLab','ResearchMaelstromRounds/FactoryTechReactor'],
               ['ResearchLockOnRangeUpgrade/FactoryTechLab','ResearchLockOnRangeUpgrade/FactoryTechReactor'],
               ['ResearchCycloneLockOnDamageUpgrade/FactoryTechLab','ResearchCycloneLockOnDamageUpgrade/FactoryTechReactor'],
               ['Research330mmBarrageCannon/FactoryTechLab','Research330mmBarrageCannon/FactoryTechReactor'],
               ['ResearchShockwaveMissileBattery/StarportTechLab','ResearchShockwaveMissileBattery/StarportTechReactor'],
               ['ResearchPhobosClassWeaponsSystem/StarportTechLab','ResearchPhobosClassWeaponsSystem/StarportTechReactor'],
               ['ResearchRipwaveMissiles/StarportTechLab','ResearchRipwaveMissiles/StarportTechReactor'],
               ['SummonNydusWorm/NydusNetwork','ZagaraVoidCoopNydusWorm/NydusNetwork'],
               ['Queen','QueenCoop'],
               ['BuildCreepTumor/Queen','BuildCreepTumor/QueenCoop'],
               ['MorphMorphalisk/Queen','MorphMorphalisk/QueenCoop'],
               ['Transfusion/Queen','Transfusion/QueenCoop'],
               ['Immortal/RoboticsFacility','Immortal/RoboticsFacilityWarp'],
               ['Colossus/RoboticsFacility','Colossus/RoboticsFacilityWarp'],
               ['Observer/RoboticsFacility','Observer/RoboticsFacilityWarp']]
			   
CONFLICT_CHECKS = [['AnionPulseCrystals/FleetBeacon', 'ResearchInterceptorLaunchSpeedUpgrade/FleetBeacon', 'Cancel'], #LotV Multiplayer/Protoss/Structures/Fleet Beacon
                   ['Zealot', 'Sentry', 'Stalker', 'WarpInAdept/Gateway', 'HighTemplar', 'DarkTemplar', 'Rally', 'UpgradeToWarpGate/Gateway', 'Cancel'], #LotV Multiplayer/Protoss/Structures/Gateway/General
                   ['Zealot', 'Sentry', 'Stalker', 'WarpInAdept/WarpGate', 'HighTemplar', 'DarkTemplar', 'Rally', 'MorphBackToGateway/WarpGate'], #LotV Multiplayer/Protoss/Structures/Gateway/Warp Gate
                   ['Probe/Nexus', 'MothershipCore/Nexus', 'Stop', 'Attack', 'Rally', 'TimeWarp/Nexus', 'Cancel'], #LotV Multiplayer/Protoss/Structures/Nexus
                   ['ResearchGraviticBooster/RoboticsBay', 'ResearchGraviticDrive/RoboticsBay', 'ResearchExtendedThermalLance/RoboticsBay', 'Cancel'], #LotV Multiplayer/Protoss/Structures/Robotics Bay
                   ['Observer/RoboticsFacility', 'WarpPrism/RoboticsFacility', 'Immortal/RoboticsFacility', 'Colossus/RoboticsFacility', 'WarpinDisruptor/RoboticsFacility', 'Rally', 'Cancel'], #LotV Multiplayer/Protoss/Structures/Robotics Facility
                   ['ResearchCharge/TwilightCouncil', 'ResearchStalkerTeleport/TwilightCouncil', 'AdeptResearchPiercingUpgrade/TwilightCouncil', 'Cancel'], #LotV Multiplayer/Protoss/Structures/Twilight Council
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'AdeptPhaseShift/Adept', 'Rally'], #LotV Multiplayer/Protoss/Units/Adept
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Interceptor/Carrier', 'ReleaseInterceptors/Carrier', 'Cancel'], #LotV Multiplayer/Protoss/Units/Carrier
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'PurificationNovaTargeted/Disruptor', 'Rally'], #LotV Multiplayer/Protoss/Units/Disruptor
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Feedback/HighTemplar', 'PsiStorm/HighTemplar', 'AWrp', 'Rally'], #LotV Multiplayer/Protoss/Units/High Templar
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'ImmortalOverload/Immortal'], #LotV Multiplayer/Protoss/Units/Immortal
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MothershipCoreWeapon/Mothership', 'MothershipMassRecall/Mothership', 'TemporalField/Mothership'], #LotV Multiplayer/Protoss/Units/Mothership
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MorphToMothership/MothershipCore', 'MothershipCoreWeapon/MothershipCore', 'MothershipCoreMassRecall/MothershipCore', 'TemporalField/MothershipCore', 'Cancel'], #LotV Multiplayer/Protoss/Units/Mothership Core
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'OracleAttack', 'OracleRevelation/Oracle', 'OracleBuildStasisTrap/Oracle', 'OracleWeaponOn/Oracle', 'OracleWeaponOff/Oracle', 'Cancel'], #LotV Multiplayer/Protoss/Units/Oracle
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'GravitonBeam/Phoenix', 'Cancel'], #LotV Multiplayer/Protoss/Units/Phoenix
                   ['TwilightCouncil/Probe', 'Stargate/Probe', 'RoboticsFacility/Probe', 'TemplarArchive/Probe', 'FleetBeacon/Probe', 'RoboticsBay/Probe', 'DarkShrine/Probe', 'Cancel'], #LotV Multiplayer/Protoss/Units/Probe/ProbeAdvanced Structures
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'GuardianShield/Sentry', 'ForceField/Sentry', 'Hallucination/Sentry', 'Rally'], #LotV Multiplayer/Protoss/Units/Sentry/General
                   ['ProbeHallucination/Sentry', 'ZealotHallucination/Sentry', 'AdeptHallucination/Sentry', 'StalkerHallucination/Sentry', 'ImmortalHallucination/Sentry', 'HighTemplarHallucination/Sentry', 'ArchonHallucination/Sentry', 'VoidRayHallucination/Sentry', 'PhoenixHallucination/Sentry', 'WarpPrismHallucination/Sentry', 'OracleHallucination/Sentry', 'ColossusHallucination/Sentry', 'DisruptorHallucination/Sentry', 'Cancel'], #LotV Multiplayer/Protoss/Units/Sentry/Hallucinations
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Blink/Stalker', 'Rally'], #LotV Multiplayer/Protoss/Units/Stalker
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'VoidRaySwarmDamageBoost/VoidRay'], #LotV Multiplayer/Protoss/Units/Void Ray
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'PhasingMode/WarpPrism', 'TransportMode/WarpPrism', 'BunkerLoad', 'BunkerUnloadAll'], #LotV Multiplayer/Protoss/Units/Warp Prism
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Charge/Zealot', 'Rally'], #LotV Multiplayer/Protoss/Units/Zealot
                   ['TerranVehicleWeaponsLevel1/Armory', 'TerranVehicleAndShipPlatingLevel1/Armory', 'TerranShipWeaponsLevel1/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #LotV Multiplayer/Terran/Structures/Armory
                   ['TerranInfantryWeaponsLevel1/EngineeringBay', 'TerranInfantryArmorLevel1/EngineeringBay', 'ResearchHiSecAutoTracking/EngineeringBay', 'ResearchNeosteelFrame/EngineeringBay', 'UpgradeBuildingArmorLevel1/EngineeringBay', 'SelectBuilder', 'Halt', 'Cancel'], #LotV Multiplayer/Terran/Structures/Barracks/Engineering BayGeneral
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'TechLabBarracks/BarracksFlying', 'Reactor/BarracksFlying', 'Land'], #LotV Multiplayer/Terran/Structures/Barracks/Flying
                   ['Marine/Barracks', 'Reaper/Barracks', 'Marauder/Barracks', 'Ghost/Barracks', 'SelectBuilder', 'Rally', 'TechLabBarracks/Barracks', 'Reactor/Barracks', 'Lift', 'Halt', 'Cancel'], #LotV Multiplayer/Terran/Structures/Barracks/General
                   ['SelectBuilder', 'SetBunkerRallyPoint/Bunker', 'Halt', 'Cancel'], #LotV Multiplayer/Terran/Structures/Bunker/Construction
                   ['Stop', 'Attack', 'SelectBuilder', 'SetBunkerRallyPoint/Bunker', 'Stim', 'BunkerLoad', 'BunkerUnloadAll', 'Salvage/Bunker', 'Cancel'], #LotV Multiplayer/Terran/Structures/Bunker/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'CommandCenterLoad', 'CommandCenterUnloadAll', 'Land'], #LotV Multiplayer/Terran/Structures/Command Center/Flying
                   ['SCV', 'OrbitalCommand/CommandCenter', 'UpgradeToPlanetaryFortress/CommandCenter', 'SelectBuilder', 'Rally', 'CommandCenterLoad', 'CommandCenterUnloadAll', 'Lift', 'Halt', 'Cancel'], #LotV Multiplayer/Terran/Structures/Command Center/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'BuildTechLabFactory/FactoryFlying', 'Reactor/FactoryFlying', 'Land'], #LotV Multiplayer/Terran/Structures/Factory/Flying
                   ['Hellion/Factory', 'WidowMine/Factory', 'SiegeTank/Factory', 'BuildCyclone/Factory', 'HellionTank/Factory', 'Thor/Factory', 'SelectBuilder', 'Rally', 'TechLabFactory/Factory', 'Reactor/Factory', 'Lift', 'Cancel'], #LotV Multiplayer/Terran/Structures/Factory/General
                   ['ResearchBattlecruiserSpecializations/FusionCore', 'ResearchBattlecruiserEnergyUpgrade/FusionCore', 'SelectBuilder', 'Halt', 'Cancel'], #LotV Multiplayer/Terran/Structures/Fusion Core
                   ['SCV', 'Rally', 'CalldownMULE/OrbitalCommand', 'SupplyDrop/OrbitalCommand', 'Scan/OrbitalCommand', 'Lift', 'Cancel'], #LotV Multiplayer/Terran/Structures/Orbital Command
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'BuildTechLabStarport/StarportFlying', 'Reactor/StarportFlying', 'Land'], #LotV Multiplayer/Terran/Structures/Starport/Flying
                   ['VikingFighter/Starport', 'Medivac/Starport', 'Liberator/Starport', 'Raven/Starport', 'Banshee/Starport', 'Battlecruiser/Starport', 'SelectBuilder', 'Rally', 'TechLabStarport/Starport', 'Reactor/Starport', 'Lift', 'Cancel'], #LotV Multiplayer/Terran/Structures/Starport/General
                   ['SelectBuilder', 'Lower/SupplyDepot', 'Halt', 'Cancel', 'Raise/SupplyDepotLowered'], #LotV Multiplayer/Terran/Structures/Supply Depot
                   ['ResearchHighCapacityBarrels/FactoryTechLab', 'ResearchDrillClaws/FactoryTechLab', 'CycloneResearchLockOnDamageUpgrade/FactoryTechLab', 'Cancel'], #LotV Multiplayer/Terran/Structures/Tech Lab/Attached to Factory
                   ['ResearchHighCapacityFuelTanks/StarportTechLab', 'ResearchExplosiveShrapnelShells/StarportTechLab', 'ResearchRavenEnergyUpgrade/StarportTechLab', 'ResearchBansheeCloak/StarportTechLab', 'BansheeSpeed/StarportTechLab', 'ResearchBallisticRange/StarportTechLab', 'Cancel'], #LotV Multiplayer/Terran/Structures/Tech Lab/Attached to Starport
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'CloakOnBanshee', 'CloakOff', 'GhostHoldFire/Ghost', 'WeaponsFree/Ghost', 'ChannelSnipe/Ghost', 'EMP/Ghost', 'NukeCalldown/Ghost', 'Cancel'], #LotV Multiplayer/Terran/Units/Ghost
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'LiberatorAGMode/Liberator', 'LiberatorAAMode/Liberator'], #LotV Multiplayer/Terran/Units/Liberator
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Heal/Medivac', 'MedivacSpeedBoost/Medivac', 'BunkerLoad', 'BunkerUnloadAll'], #LotV Multiplayer/Terran/Units/Medivac
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'AutoTurret/Raven', 'PointDefenseDrone/Raven', 'HunterSeekerMissile/Raven'], #LotV Multiplayer/Terran/Units/Raven
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'KD8Charge/Reaper'], #LotV Multiplayer/Terran/Units/Reaper
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'GatherProt', 'ReturnCargo', 'TerranBuild/SCV', 'TerranBuildAdvanced/SCV', 'Repair', 'Halt'], #LotV Multiplayer/Terran/Units/SCV/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'WidowMineBurrow/WidowMine', 'WidowMineUnburrow/WidowMine'], #LotV Multiplayer/Terran/Units/Widow Mine
                   ['BuildCreepTumorPropagate/CreepTumorBurrowed', 'Cancel'], #LotV Multiplayer/Zerg/Structures/Creep Tumor
                   ['hydraliskspeed/HydraliskDen', 'MutateintoLurkerDen/HydraliskDen', 'Cancel'], #LotV Multiplayer/Zerg/Structures/Hydralisk Den
                   ['hydraliskspeed/LurkerDenMP', 'Cancel'], #LotV Multiplayer/Zerg/Structures/Lurker Den
                   ['Stop', 'SummonNydusWorm/NydusNetwork', 'Rally', 'BunkerLoad', 'BunkerUnloadAll', 'Cancel'], #LotV Multiplayer/Zerg/Structures/Nydus Network
                   ['Stop', 'Attack', 'SpineCrawlerUproot/SpineCrawler', 'Cancel'], #LotV Multiplayer/Zerg/Structures/Spine Crawler/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'SpineCrawlerRoot/SpineCrawlerUprooted', 'Cancel'], #LotV Multiplayer/Zerg/Structures/Spine Crawler/Uprooted
                   ['zergflyerattack1', 'zergflyerarmor1', 'GreaterSpire/Spire', 'Cancel'], #LotV Multiplayer/Zerg/Structures/Spire
                   ['Stop', 'Attack', 'SporeCrawlerUproot/SporeCrawler', 'Cancel'], #LotV Multiplayer/Zerg/Structures/Spore Crawler/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'SporeCrawlerRoot/SporeCrawlerUprooted', 'Cancel'], #LotV Multiplayer/Zerg/Structures/Spore Crawler/Uprooted
                   ['Attack', 'Explode/BanelingBurrowed', 'BurrowUp'], #LotV Multiplayer/Zerg/Units/Baneling/Burrowed
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Explode/Baneling', 'EnableBuildingAttack/Baneling', 'DisableBuildingAttack/Baneling', 'BurrowDown'], #LotV Multiplayer/Zerg/Units/Baneling/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'CausticSpray/Corruptor', 'BroodLord/Corruptor', 'Cancel'], #LotV Multiplayer/Zerg/Units/Corruptor
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'GatherProt', 'ReturnCargo', 'ZergBuild/Drone', 'ZergBuildAdvanced/Drone', 'BurrowDown'], #LotV Multiplayer/Zerg/Units/Drone/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MorphToOverseer/Overlord', 'StopGenerateCreep', 'BunkerLoad', 'BunkerUnloadAll', 'Cancel'], #LotV Multiplayer/Zerg/Units/Droplord/Creeping
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MorphToOverseer/Overlord', 'GenerateCreep/Overlord', 'BunkerLoad', 'BunkerUnloadAll', 'Cancel'], #LotV Multiplayer/Zerg/Units/Droplord/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'LurkerMP/Hydralisk', 'BurrowDown'], #LotV Multiplayer/Zerg/Units/Hydralisk
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'InfestedTerrans/InfestorBurrowed', 'BurrowUp'], #LotV Multiplayer/Zerg/Units/Infestor/Burrowed
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'InfestedTerrans/Infestor', 'FungalGrowth/Infestor', 'NeuralParasite/Infestor', 'Cancel', 'BurrowDown'], #LotV Multiplayer/Zerg/Units/Infestor/General
                   ['Drone/Larva', 'Overlord/Larva', 'Zergling/Larva', 'Roach/Larva', 'Hydralisk/Larva', 'Mutalisk/Larva', 'Corruptor/Larva', 'Infestor/Larva', 'SwarmHostMP/Larva', 'Viper/Larva', 'Ultralisk/Larva', 'Cancel'], #LotV Multiplayer/Zerg/Units/Larva/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'LocustMPFlyingSwoop/LocustMPFlying'], #LotV Multiplayer/Zerg/Units/Locust (Flying)
                   ['Stop', 'Attack', 'LurkerHoldFire/LurkerMPBurrowed', 'LurkerCancelHoldFire/LurkerMPBurrowed', 'LurkerBurrowUp'], #LotV Multiplayer/Zerg/Units/Lurker/Burrowed
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'BurrowLurkerMP'], #LotV Multiplayer/Zerg/Units/Lurker/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MorphToOverseer/Overlord', 'StopGenerateCreep', 'MorphtoOverlordTransport/Overlord', 'BunkerUnloadAll', 'Cancel'], #LotV Multiplayer/Zerg/Units/Overlord/Creeping (BunkerUnloadAll shouldn't be here)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MorphToOverseer/Overlord', 'GenerateCreep/Overlord', 'MorphtoOverlordTransport/Overlord', 'BunkerUnloadAll', 'Cancel'], #LotV Multiplayer/Zerg/Units/Overlord/General (BunkerUnloadAll shouldn't be here)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'SpawnChangeling/Overseer', 'Contaminate/Overseer'], #LotV Multiplayer/Zerg/Units/Overseer
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'BuildCreepTumor/Queen', 'MorphMorphalisk/Queen', 'Transfusion/Queen', 'BurrowDown'], #LotV Multiplayer/Zerg/Units/Queen
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'RavagerCorrosiveBile/Ravager', 'BurrowDown'], #LotV Multiplayer/Zerg/Units/Ravager
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Ravager/Roach', 'BurrowDown'], #LotV Multiplayer/Zerg/Units/Roach
                   ['Attack', 'VoidSwarmHostSpawnLocust/SwarmHostBurrowedMP', 'SwarmHostBurrowUp'], #LotV Multiplayer/Zerg/Units/Swarm Host/Burrowed
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'SwarmHost/SwarmHostMP', 'SwarmHostBurrowDown'], #LotV Multiplayer/Zerg/Units/Swarm Host/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'ViperConsume/Viper', 'FaceEmbrace/Viper', 'BlindingCloud/Viper', 'ParasiticBomb/Viper'], #LotV Multiplayer/Zerg/Units/Viper
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Baneling/Zergling', 'BurrowDown'], #LotV Multiplayer/Zerg/Units/Zergling
                   ['Stop', 'Attack', 'DarkPylonRecall/DarkPylon', 'Cancel'], #Coop/Protoss Story/Structures/Dark Pylon
                   ['ShieldBatteryRecharge/ShieldBattery', 'ShieldBatteryStructureBarrier/ShieldBattery', 'Cancel'], #Coop/Protoss Story/Structures/Shield Battery
                   ['ResearchSolarEfficiencyLevel1/SolarForge', 'ResearchSOARepairBeamExtraTarget/SolarForge', 'ResearchSOAOrbitalStrikeUpgrade/SolarForge', 'ResearchSOASolarLanceUpgrade/SolarForge', 'Cancel'], #Coop/Protoss Story/Structures/Solar Forge (Karax Commander)/General
                   ['BrokenSolarForge/SolarForge'], #Coop/Protoss Story/Structures/Solar Forge (Karax Commander)/General (Broken)
                   ['Immortal/RoboticsFacilityWarp', 'Colossus/RoboticsFacilityWarp', 'Observer/RoboticsFacilityWarp', 'MorphBackToRoboticsFacility/RoboticsFacilityWarp', 'Cancel'], #Coop/Protoss Story/Structures/Warp Robotics Facility
                   ['Phoenix/StargateWarp', 'VoidRay/StargateWarp', 'Oracle/StargateWarp', 'Arbiter/StargateWarp', 'MorphBackToStargate/StargateWarp', 'Cancel'], #Coop/Protoss Story/Structures/Warp Stargate
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'ImmortalShakurasShadowCannon/ImmortalShakuras'], #Coop/Protoss Story/Units/Annihilator
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'VoidHighTemplarPsiOrb/HighTemplarTaldarim', 'VoidHighTemplarMindBlast/HighTemplarTaldarim', 'AscendantSacrifice/HighTemplarTaldarim', 'Rally'], #Coop/Protoss Story/Units/Ascendant
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'VoidStasis/DarkTemplarTaldarim', 'Rally'], #Coop/Protoss Story/Units/Blood Hunter
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Interceptor/CarrierAiur', 'Cancel'], #Coop/Protoss Story/Units/Carrier
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'VoidZealotShadowCharge/ZealotShakuras', 'VoidZealotShadowChargeStun/ZealotShakuras', 'Rally'], #Coop/Protoss Story/Units/Centurion (Vorazun Commander)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'CorsairMPDisruptionWeb/CorsairMP', 'Rally'], #Coop/Protoss Story/Units/Corsair
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'VoidDarkTemplarShadowFury/DarkTemplarShakuras', 'DarkTemplarShadowDash/DarkTemplarShakuras', 'VoidStasis/DarkTemplarShakuras', 'Rally'], #Coop/Protoss Story/Units/Dark Templar (Vorazun Commander)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'VoidSentryChronoBeam/SentryPurifier', 'EnergizerReclamation/SentryPurifier', 'VoidSentryPhasingMode/SentryPurifier', 'VoidSentryMobileMode/SentryPurifier', 'Rally'], #Coop/Protoss Story/Units/Energizer (Karax Commander)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'TargetLock/Monitor', 'SentryTaldarimForceField/Monitor', 'Rally'], #Coop/Protoss Story/Units/Havoc
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Feedback/HighArchonTemplar', 'HighArchonPsiStorm/HighArchonTemplar', 'ArchonAdvancedMergeSelection', 'Rally'], #Coop/Protoss Story/Units/High Templar
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'ImmortalOverload/ImmortalAiur', 'ImmortalShakurasShadowCannon/ImmortalAiur'], #Coop/Protoss Story/Units/Immortal
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'GravitonBeamVoidCampaign/PhoenixPurifier', 'Cancel'], #Coop/Protoss Story/Units/Mirage
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'VoidSentryBlackHole/SOAMothershipv4', 'SOAMothershipLineAttack/SOAMothershipv4', 'SOAMothershipBlink/SOAMothershipv4'], #Coop/Protoss Story/Units/Mothership
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Charge/ZealotPurifier', 'Rally'], #Coop/Protoss Story/Units/Sentinel (Karax Commander)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'VoidSentryShieldRepairDouble/SentryAiur', 'GuardianShield/SentryAiur', 'Rally'], #Coop/Protoss Story/Units/Sentry
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'VoidShadowGuardShadowFury/VorazunShadowGuard', 'ShadowGuardBlink/VorazunShadowGuard', 'VoidStasis/VorazunShadowGuard'], #Coop/Protoss Story/Units/Shadow Guard
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'StalkerBlinkShieldRestoreBase/StalkerShakuras', 'Rally'], #Coop/Protoss Story/Units/Stalker
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'LightningBomb/TempestPurifier', 'Rally'], #Coop/Protoss Story/Units/Tempest
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Charge/ZealotAiur', 'VoidZealotWhirlwind/ZealotAiur', 'Rally'], #Coop/Protoss Story/Units/Zealot (Artanis Commander)
                   ['ResearchShadowFury/DarkShrine', 'ResearchShadowDash/DarkShrine', 'ResearchVoidStasis/DarkShrine', 'ResearchDarkArchonFullStartingEnergy/DarkShrine', 'ResearchDarkArchonMindControl/DarkShrine', 'Cancel'], #Coop/Protoss/Structures/Dark Shrine (Vorazun Commander)
                   ['AnionPulseCrystals/FleetBeacon', 'ResearchDoubleGravitonBeam/FleetBeacon', 'ResearchTempestDisintegration/FleetBeacon', 'ResearchOracleStasisWardUpgrade/FleetBeacon', 'Cancel'], #Coop/Protoss/Structures/Fleet Beacon (Artanis+Vorazun Commander)
                   ['ProtossGroundWeaponsLevel1/Forge', 'ProtossGroundArmorLevel1/Forge', 'ProtossShieldsLevel1/Forge', 'ResearchKaraxTurretRange/Forge', 'ResearchKaraxTurretAttackSpeed/Forge', 'ResearchStructureBarrier/Forge', 'Cancel'], #Coop/Protoss/Structures/Forge (Karax Commander)
                   ['Zealot', 'Sentry', 'Stalker', 'HighTemplar', 'DarkTemplar', 'DarkArchon/Gateway', 'Rally', 'UpgradeToWarpGate/Gateway', 'Cancel'], #Coop/Protoss/Structures/Gateway/General (Gateway)
                   ['Zealot', 'Sentry', 'Stalker', 'HighTemplar', 'DarkTemplar', 'DarkArchon/WarpGate', 'Rally', 'MorphBackToGateway/WarpGate', 'Cancel'], #Coop/Protoss/Structures/Gateway/Warp Gate
                   ['Probe/Nexus', 'Mothership/Nexus', 'Stop', 'Attack', 'Rally', 'TimeWarp/Nexus', 'Cancel'], #Coop/Protoss/Structures/Nexus
                   ['ResearchGraviticBooster/RoboticsBay', 'ResearchBarrier/RoboticsBay', 'ResearchReaverIncreasedScarabCount/RoboticsBay', 'ResearchReaverIncreasedScarabSplashRadius/RoboticsBay', 'Cancel'], #Coop/Protoss/Structures/Robotics Bay (Artanis Commander)
                   ['ResearchGraviticBooster/RoboticsBay', 'ResearchExtendedThermalLance/RoboticsBay', 'ResearchReaverIncreasedScarabSplashRadius/RoboticsBay', 'ResearchBarrier/RoboticsBay', 'Cancel'], #Coop/Protoss/Structures/Robotics Bay (Karax Commander)(not tested)
                   ['Immortal/RoboticsFacility', 'Colossus/RoboticsFacility', 'Observer/RoboticsFacility', 'Rally', 'UpgradeToRoboticsFacilityWarp/RoboticsFacility', 'Cancel'], #Coop/Protoss/Structures/Robotics Facility
                   ['Phoenix/Stargate', 'VoidRay/Stargate', 'Oracle/Stargate', 'Arbiter/Stargate', 'Rally', 'UpgradeToStargateWarp/Stargate', 'Cancel'], #Coop/Protoss/Structures/Stargate
                   ['ResearchPsiStorm/TemplarArchive', 'ResearchHighTemplarEnergyUpgrade/TemplarArchive', 'ResearchHealingPsionicStorm/TemplarArchive', 'Cancel'], #Coop/Protoss/Structures/Templar Archives (Artanis Commander)
                   ['ResearchCharge/TwilightCouncil', 'ResearchDragoonRange/TwilightCouncil', 'ResearchWhirlwind/TwilightCouncil', 'ResearchDragoonChassis/TwilightCouncil', 'Cancel'], #Coop/Protoss/Structures/Twilight Council (Artanis commander)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'ArbiterMPStasisField/ArbiterMP', 'ArbiterMPRecall/ArbiterMP', 'Rally'], #Coop/Protoss/Units/Arbiter
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Feedback/Archon', 'PsiStorm/Archon', 'Rally'], #Coop/Protoss/Units/Archon
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'DarkArchonConfusion/DarkArchon', 'DarkArchonMindControl/DarkArchon', 'Rally'], #Coop/Protoss/Units/Dark Archon
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MorphtoObserverSiege/Observer', 'MorphtoObserver/Observer'], #Coop/Protoss/Units/Observer
                   ['Nexus/Probe', 'Assimilator/Probe', 'Pylon/Probe', 'Gateway/Probe', 'Forge/Probe', 'ShieldBattery/Probe', 'CyberneticsCore/Probe', 'PhotonCannon/Probe', 'KhaydarinMonolith/Probe', 'Cancel'], #Coop/Protoss/Units/Probe/Basic Structures
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'ReaverScarabs/Reaver', 'Rally'], #Coop/Protoss/Units/Reaver
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'VoidSentryShieldRepair/Sentry', 'GuardianShield/Sentry', 'ForceField/Sentry', 'Rally'], #Coop/Protoss/Units/Sentry/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'LightningBomb/Tempest', 'Rally'], #Coop/Protoss/Units/TempestGeneral
                   ['Stop', 'Attack', 'SelectBuilder', 'Salvage/KelMorianGrenadeTurret', 'Halt', 'Cancel'], #Coop/Terran Story/Structures/Devastation Turret (Swann Commander)
                   ['Attack', 'ResearchDrakkenLaserDrillBFG/DrakkenLaserDrillCoop', 'Cancel'], #Coop/Terran Story/Structures/Drakken Laser Drill
                   ['Stop', 'Attack', 'SelectBuilder', 'Salvage/PerditionTurret', 'Halt', 'Cancel'], #Coop/Terran Story/Structures/Perdition Turret
                   ['Stop', 'Attack', 'SelectBuilder', 'Salvage/KelMorianMissileTurret', 'Halt', 'Cancel'], #Coop/Terran Story/Structures/Spinning Dizzy
                   ['ResearchShieldWall/BarracksTechReactor', 'Stimpack/BarracksTechReactor', 'ResearchPunisherGrenades/BarracksTechReactor', 'ResearchIncineratorGauntlets/BarracksTechReactor', 'ResearchJuggernautPlating/BarracksTechReactor', 'ResearchStabilizerMedpacks/BarracksTechReactor', 'Cancel'], #Coop/Terran Story/Structures/Tech Reactor/Attached to Barracks (Raynor Commander, notAvailable)
                   ['ResearchHighCapacityBarrels/FactoryTechReactor', 'ResearchHellbatHellArmor/FactoryTechReactor', 'ResearchAresClassTargetingSystem/FactoryTechReactor', 'ResearchMultiLockWeaponsSystem/FactoryTechReactor', 'ResearchMaelstromRounds/FactoryTechReactor', 'ResearchLockOnRangeUpgrade/FactoryTechReactor', 'ResearchCycloneLockOnDamageUpgrade/FactoryTechReactor', 'Research330mmBarrageCannon/FactoryTechReactor', 'Cancel'], #Coop/Terran Story/Structures/Tech Reactor/Attached to Factory (Swann Commander)
                   ['ResearchBansheeCloak/StarportTechReactor', 'ResearchShockwaveMissileBattery/StarportTechReactor', 'ResearchPhobosClassWeaponsSystem/StarportTechReactor', 'ResearchRipwaveMissiles/StarportTechReactor', 'Cancel'], #Coop/Terran Story/Structures/Tech Reactor/Attached to Starport (Raynor(+Swann) Commander)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'HerculesLoad/Hercules', 'HerculesUnloadAll/Hercules', 'HyperjumpHercules/Hercules'], #Coop/Terran Story/Units/Hercules (Swann Commander)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'HyperionVoidCoopHyperjump/HyperionVoidCoop', 'HyperionVoidCoopYamatoCannon/HyperionVoidCoop', 'HyperionAdvancedPDD/HyperionVoidCoop'], #Coop/Terran Story/Units/Hyperion (Raynor Commander)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MedicHeal/Medic'], #Coop/Terran Story/Units/Medic
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'NanoRepair/ScienceVessel', 'Irradiate/ScienceVessel', 'DefensiveMatrixTarget/ScienceVessel'], #Coop/Terran Story/Units/Science Vessel (Swann Commander)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'SpectreHoldFire/Spectre', 'SpectreWeaponsFree/Spectre', 'MindBlast/Spectre', 'VoodooShield/Spectre', 'SpectreDomination/Spectre', 'NukeCalldown/Spectre', 'Cancel'], #Coop/Terran Story/Units/Spectre (Tosh framework, AI)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'SpiderMine/Vulture', 'SpiderMineReplenish/Vulture', 'IgniteAfterburners/Vulture', 'Cancel'], #Coop/Terran Story/Units/Vulture (Raynor Commander)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'WraithCloakOn/Wraith', 'WraithCloakOff/Wraith'], #Coop/Terran Story/Units/Wraith (Swann Commander)
                   ['TerranVehicleAndShipWeaponsLevel1/Armory', 'TerranVehicleAndShipPlatingLevel1/Armory', 'ResearchVehicleWeaponRange/Armory', 'ResearchRegenerativeBioSteel/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #Coop/Terran/Structures/Armory
                   ['Marine/Barracks', 'Marauder/Barracks', 'Reaper/Barracks', 'Firebat/Barracks', 'Medic/Barracks', 'HireKelmorianMiners/Barracks', 'HireHammerSecurities/Barracks', 'HireDevilDogs/Barracks', 'MercReaper/Barracks', 'MercMedic/Barracks', 'Cancel'], #Coop/Terran/Structures/Barracks (kinda Raynor Commander)/General (AI)
                   ['SCV', 'VespeneDrone/CommandCenter', 'OrbitalCommand/CommandCenter', 'SelectBuilder', 'Rally', 'CommandCenterLoad', 'CommandCenterUnloadAll', 'Lift', 'Cancel'], #Coop/Terran/Structures/Command Center/General
                   ['TerranInfantryWeaponsLevel1/EngineeringBay', 'TerranInfantryArmorLevel1/EngineeringBay', 'ResearchNeosteelFrame/EngineeringBay', 'UpgradeBuildingArmorLevel1/EngineeringBay', 'SelectBuilder', 'ResearchFireSuppressionSystems/EngineeringBay', 'ResearchImprovedTurretAttackSpeed/EngineeringBay', 'Halt', 'Cancel'], #Coop/Terran/Structures/Engineering Bay (Raynor Commander)
                   ['HellionTank/Factory', 'Goliath/Factory', 'SiegeTank/Factory', 'BuildCyclone/Factory', 'Thor/Factory', 'SelectBuilder', 'Rally', 'TechLabFactory/Factory', 'Reactor/Factory', 'Lift', 'Cancel'], #Coop/Terran/Structures/Factory/General (kinda Swann Commander)
                   ['HellionTank/Factory', 'Goliath/Factory', 'SiegeTank/Factory', 'WidowMine/Factory', 'Thor/Factory', 'MercHellion/Factory', 'HireSpartanCompany/Factory', 'HireSiegeBreakers/Factory', 'Cancel'], #Coop/Terran/Structures/Factory/General3
                   ['ResearchPersonalCloaking/GhostAcademy', 'ResearchGhostEnergyUpgrade/GhostAcademy', 'SelectBuilder', 'NukeArm/GhostAcademy', 'Halt', 'Cancel'], #Coop/Terran/Structures/Ghost Academy
                   ['Stop', 'Attack', 'SelectBuilder', 'Salvage/MissileTurret', 'Halt', 'Cancel'], #Coop/Terran/Structures/Missile Turret
                   ['SCV', 'VespeneDrone/PlanetaryFortress', 'StopPlanetaryFortress/PlanetaryFortress', 'Attack', 'Rally', 'CommandCenterLoad', 'CommandCenterUnloadAll', 'Cancel'], #Coop/Terran/Structures/Planetary Fortress
                   ['VikingFighter/Starport', 'Banshee/Starport', 'Wraith/Starport', 'Battlecruiser/Starport', 'HireDuskWing/Starport', 'HireHelsAngels/Starport', 'HireDukesRevenge/Starport', 'Cancel'], #Coop/Terran/Structures/Starport/General3
                   ['ResearchShieldWall/BarracksTechLab', 'Stimpack/BarracksTechLab', 'ResearchPunisherGrenades/BarracksTechLab', 'ResearchIncineratorGauntlets/BarracksTechLab', 'ResearchJuggernautPlating/BarracksTechLab', 'ResearchStabilizerMedpacks/BarracksTechLab', 'Cancel'], #Coop/Terran/Structures/Tech Lab/Attached to Barracks (Raynor Commander)
                   ['ResearchHighCapacityBarrels/FactoryTechLab', 'ResearchHellbatHellArmor/FactoryTechLab', 'ResearchAresClassTargetingSystem/FactoryTechLab', 'ResearchMultiLockWeaponsSystem/FactoryTechLab', 'ResearchMaelstromRounds/FactoryTechLab', 'ResearchLockOnRangeUpgrade/FactoryTechLab', 'ResearchCycloneLockOnDamageUpgrade/FactoryTechLab', 'Research330mmBarrageCannon/FactoryTechLab', 'Cancel'], #Coop/Terran/Structures/Tech Lab/Attached to Factory (Swann(+Raynor) Commander)
                   ['ResearchBansheeCloak/StarportTechLab', 'ResearchShockwaveMissileBattery/StarportTechLab', 'ResearchPhobosClassWeaponsSystem/StarportTechLab', 'ResearchRipwaveMissiles/StarportTechLab', 'Cancel'], #Coop/Terran/Structures/Tech Lab/Attached to Starport (Raynor(+Swann) Commander)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'CloakOnBanshee', 'CloakOff', 'IgniteAfterburners/Banshee'], #Coop/Terran/Units/Banshee (Raynor Commander)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'YamatoGun', 'Hyperjump/Battlecruiser', 'IgniteAfterburners/Battlecruiser'], #Coop/Terran/Units/Battlecruiser (Raynor Commander)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'LockOn/Cyclone', 'SwannCommanderRebuild', 'Cancel'], #Coop/Terran/Units/Cyclone
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'CloakOnBanshee', 'CloakOff', 'GhostHoldFire/Ghost', 'WeaponsFree/Ghost', 'Snipe/Ghost', 'EMP/Ghost', 'NukeCalldown/Ghost', 'Cancel'], #Coop/Terran/Units/Ghost
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MorphToHellion/Hellion', 'MorphToHellionTank/Hellion', 'SwannCommanderRebuild'], #Coop/Terran/Units/Hellion (Swann Commander)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'LiberatorAGMode/Liberator', 'IgniteAfterburners/Liberator'], #Coop/Terran/Units/Liberator
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'AutoTurret/Raven', 'PointDefenseDrone/Raven', 'InstantHunterSeekerMissile/Raven'], #Coop/Terran/Units/Raven
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'D8Charge/Reaper'], #Coop/Terran/Units/Reaper (WoL Campaign)
                   ['GhostAcademy/SCV', 'MercCompound/SCV', 'Factory/SCV', 'Armory/SCV', 'Starport/SCV', 'FusionCore/SCV', 'Cancel'], #Coop/Terran/Units/SCV/Advanced Structures
                   ['CommandCenter/SCV', 'Refinery/SCV', 'SupplyDepot/SCV', 'Barracks/SCV', 'EngineeringBay/SCV', 'Bunker/SCV', 'MissileTurret/SCV', 'BuildKelMorianRocketTurret/SCV', 'HiveMindEmulator/SCV', 'Cancel'], #Coop/Terran/Units/SCV/Basic Structures
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'SiegeMode', 'Unsiege', 'IgniteAfterburners/SiegeTank'], #Coop/Terran/Units/Siege Tank/General (Raynor Commander)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'SiegeMode', 'SwannCommanderRebuild'], #Coop/Terran/Units/Siege Tank/General (Wreckage,Swann Commander)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', '250mmStrikeCannons/Thor', 'ThorDefensiveMatrix/Thor', 'SelfRepair/Thor', 'Cancel'], #Coop/Terran/Units/Thor (Swann Commander)/Front 01
                   ['ImmortalityProtocol/ThorWreckage', 'Cancel'], #Coop/Terran/Units/Thor (Swann Commander)/Front 02
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', '250mmStrikeCannons/ThorWreckageSwann', 'ThorDefensiveMatrix/ThorWreckageSwann', 'SelfRepair/ThorWreckageSwann', 'Cancel'], #Coop/Terran/Units/Thor (Swann Commander)/Front 03
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'FighterMode', 'AssaultMode', 'IgniteAfterburners/VikingAssault'], #Coop/Terran/Units/Viking (Raynor Commander)
                   ['BileLauncherBombardment/BileLauncherZagara', 'Cancel'], #Coop/Zerg Story/Structures/Bile Launcher (Zagara Commander)
                   ['EvolveMuscularAugments/ImpalerDen', 'EvolveAncillaryCarapace/ImpalerDen', 'EvolveFrenzy/ImpalerDen', 'Cancel'], #Coop/Zerg Story/Structures/Impaler Den
                   ['EvolveMuscularAugments/LurkerDen', 'EvolveAncillaryCarapace/LurkerDen', 'EvolveFrenzy/LurkerDen', 'ResearchLurkerRange/LurkerDen', 'Cancel'], #Coop/Zerg Story/Structures/Lurker Den
                   ['zergflyerattack1', 'zergflyerarmor1', 'EvolveScourgeSplashDamage/ScourgeNest', 'EvolveScourgeGasCostReduction/ScourgeNest'], #Coop/Zerg Story/Structures/Scourge Nest
                   ['Attack', 'Explode/HotSSplitterlingBigBurrowed', 'BurrowUp', 'Attack', 'Explode/HotSHunterBurrowed', 'BurrowUp'], #Coop/Zerg Story/Units/Baneling/Burrowed
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Explode/HotSHunter', 'EnableBuildingAttack/HotSHunter', 'BurrowDown'], #Coop/Zerg Story/Units/Baneling/Hunter Strain
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Impaler/HydraliskImpaler', 'HydraliskFrenzy/HydraliskImpaler', 'BurrowDown'], #Coop/Zerg Story/Units/Hydralisk (Impaler Strain)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Lurker/HydraliskLurker', 'HydraliskFrenzy/HydraliskLurker', 'BurrowDown'], #Coop/Zerg Story/Units/Hydralisk (Lurker Strain)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MindBolt/K5KerriganBurrowed', 'PsionicLift/K5KerriganBurrowed', 'KerriganVoidCoopEconDrop/K5KerriganBurrowed', 'KerriganVoidCoopCrushingGripWave/K5KerriganBurrowed', 'BurrowUp'], #Coop/Zerg Story/Units/Kerrigan/Burrowed
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MindBolt/K5Kerrigan', 'PsionicLift/K5Kerrigan', 'KerriganVoidCoopEconDrop/K5Kerrigan', 'KerriganVoidCoopCrushingGripWave/K5Kerrigan', 'BurrowDown'], #Coop/Zerg Story/Units/Kerrigan/General
                   ['Stop', 'Attack', 'LurkerHoldFire/LurkerBurrowed', 'LurkerCancelHoldFire/LurkerBurrowed', 'LurkerBurrowUp'], #Coop/Zerg Story/Units/Lurker (Burrowed)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'BroodLord/MutaliskBroodlord'], #Coop/Zerg Story/Units/Mutalisk (Brood Lord Strain)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Viper/MutaliskViper'], #Coop/Zerg Story/Units/Mutalisk (Viper Strain)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'DetonateScourge/Scourge', 'DisableBuildingAttackScourge/Scourge'], #Coop/Zerg Story/Units/Scourge/Building Attack Enabled
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'DetonateScourge/Scourge', 'EnableBuildingAttackScourge/Scourge'], #Coop/Zerg Story/Units/Scourge/General
                   ['Stop', 'Attack', 'LocustLaunch/SwarmHostBurrowed', 'SwarmHostUprootUnburrow', 'Stop', 'Attack', 'LocustFlyingLaunch/SwarmHostSplitABurrowed', 'SwarmHostUprootUnburrow', 'Stop', 'Attack', 'LocustLaunchCreeper/SwarmHostSplitBBurrowed', 'SwarmHostDeepBurrow/SwarmHostSplitBBurrowed', 'SwarmHostUprootUnburrow'], #Coop/Zerg Story/Units/Swarm Host/Burrowed
                   ['Stop', 'Attack', 'LocustLaunch/SwarmHostRooted', 'SwarmHostUproot', 'Stop', 'Attack', 'LocustFlyingLaunch/SwarmHostSplitARooted', 'SwarmHostUproot', 'Stop', 'Attack', 'LocustLaunchCreeper/SwarmHostSplitBRooted', 'SwarmHostDeepBurrow/SwarmHostSplitBRooted', 'SwarmHostUproot'], #Coop/Zerg Story/Units/Swarm Host/Rooted
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'PoisonNova/HotSNoxious', 'BurrowChargeCampaignNoxious/HotSNoxious', 'BurrowDown'], #Coop/Zerg Story/Units/Ultralisk (Noxious Strain)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'ZagaraVoidCoopBanelingBarrage/ZagaraVoidCoopBurrowed', 'ZagaraVoidCoopSpawnHunterKillers/ZagaraVoidCoopBurrowed', 'ZagaraVoidCoopMassFrenzy/ZagaraVoidCoopBurrowed', 'MassRoachDrop/ZagaraVoidCoopBurrowed', 'BurrowUp'], #Coop/Zerg Story/Units/Zagara/Burrowed
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'ZagaraVoidCoopBanelingBarrage/ZagaraVoidCoop', 'ZagaraVoidCoopSpawnHunterKillers/ZagaraVoidCoop', 'ZagaraVoidCoopMassFrenzy/ZagaraVoidCoop', 'MassRoachDrop/ZagaraVoidCoop', 'BurrowDown'], #Coop/Zerg Story/Units/Zagara/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Baneling/HotSRaptor', 'BurrowDown'], #Coop/Zerg Story/Units/Zergling (Raptor Strain)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Baneling/HotSSwarmling', 'BurrowDown'], #Coop/Zerg Story/Units/Zergling (Swarmling Strain)
                   ['EvolveCentrificalHooks/BanelingNest', 'EvolveBanelingCorrosiveBile/BanelingNest', 'EvolveBanelingRupture/BanelingNest', 'EvolveBanelingHeal/BanelingNest', 'Rally', 'ZagaraVoidCoopBanelingSpawner/BanelingNest', 'Cancel'], #Coop/Zerg/Structures/Baneling Nest (Zagara Commander)
                   ['zergmeleeweapons1/EvolutionChamber', 'zergmissileweapons1/EvolutionChamber', 'zerggroundarmor1/EvolutionChamber', 'EvolveKerriganHeroicFortitude/EvolutionChamber', 'EvolveK5ChainLightning/EvolutionChamber', 'EvolveK5Cooldowns/EvolutionChamber', 'Cancel'], #Coop/Zerg/Structures/Evolution Chamber (Kerrigan+Zagara Commander)
                   ['zergflyerattack1', 'zergflyerarmor1', 'EvolveMutaliskRapidRegeneration/GreaterSpire', 'EvolveViciousGlaive/GreaterSpire', 'EvolveSunderingGlave/GreaterSpire', 'EvolveBroodLordSpeed/GreaterSpire', 'Cancel'], #Coop/Zerg/Structures/Greater Spire
                   ['Larva', 'QueenCoop', 'RespawnZergling/Hatchery', 'overlordspeed', 'EvolveVentralSacks', 'RallyEgg', 'Rally', 'Lair/Hatchery', 'Cancel'], #Coop/Zerg/Structures/Hatchery
                   ['Larva', 'QueenCoop', 'RespawnZergling/Hive', 'overlordspeed', 'EvolveVentralSacks', 'RallyEgg', 'Rally', 'Cancel'], #Coop/Zerg/Structures/Hive
                   ['EvolveMuscularAugments/HydraliskDen', 'EvolveAncillaryCarapace/HydraliskDen', 'EvolveFrenzy/HydraliskDen', 'ResearchLurkerRange/HydraliskDen', 'LurkerDen/HydraliskDen', 'Cancel'], #Coop/Zerg/Structures/Hydralisk Den (Kerrigan Commander)
                   ['EvolveInfestorEnergyUpgrade/InfestationPit', 'RapidIncubation/InfestationPit', 'HotSPressurizedGlands/InfestationPit', 'Cancel'], #Coop/Zerg/Structures/Infestation Pit
                   ['Larva', 'QueenCoop', 'RespawnZergling/Lair', 'overlordspeed', 'EvolveVentralSacks', 'RallyEgg', 'Rally', 'Hive/Lair', 'Cancel'], #Coop/Zerg/Structures/Lair
                   ['Stop', 'ZagaraVoidCoopNydusWorm/NydusNetwork', 'Rally', 'BunkerLoad', 'BunkerUnloadAll', 'Cancel'], #Coop/Zerg/Structures/Nydus Network (Kerrigan Commander)
                   ['EvolveGlialRegeneration/RoachWarren', 'EvolveTunnelingClaws/RoachWarren', 'EvolveHydriodicBile/RoachWarren', 'EvolveAdaptivePlating/RoachWarren', 'Cancel'], #Coop/Zerg/Structures/Roach Warren (Kerrigan Commander)
                   ['zerglingmovementspeed/SpawningPool', 'EvolveHardenedCarapace/SpawningPool', 'zerglingattackspeed/SpawningPool', 'EvolveZerglingArmorShred/SpawningPool', 'EvolveBileLauncherIncreasedRange/SpawningPool', 'EvolveBileLauncherBombardmentCooldown/SpawningPool', 'Cancel'], #Coop/Zerg/Structures/Spawning Pool (Zagara Commander)
                   ['zergflyerattack1', 'zergflyerarmor1', 'EvolveMutaliskRapidRegeneration/Spire', 'EvolveViciousGlaive/Spire', 'EvolveSunderingGlave/Spire', 'EvolveBroodLordSpeed/Spire', 'GreaterSpireBroodlord/Spire', 'Cancel'], #Coop/Zerg/Structures/Spire
                   ['EvolveChitinousPlating/UltraliskCavern', 'EvolveBurrowCharge/UltraliskCavern', 'EvolveTissueAssimilation/UltraliskCavern', 'Cancel'], #Coop/Zerg/Structures/Ultralisk Cavern (Kerrigan Commander)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'CorruptionAbility/Corruptor', 'BroodLord/Corruptor', 'Cancel'], #Coop/Zerg/Units/Corruptor
                   ['HydraliskDen/Drone', 'InfestationPit/Drone', 'Spire/Drone', 'NydusNetwork/Drone', 'UltraliskCavern/Drone', 'ScourgeNest/Drone', 'Cancel'], #Coop/Zerg/Units/Drone/Advanced Structures (Zagara+Kerrigan Commander)
                   ['Hatchery/Drone', 'Extractor/Drone', 'SpawningPool/Drone', 'EvolutionChamber/Drone', 'BanelingNest/Drone', 'RoachWarren/Drone', 'SpineCrawler/Drone', 'SporeCrawler/Drone', 'ZagaraBileLauncher/Drone', 'Cancel'], #Coop/Zerg/Units/Drone/Basic Structures (Zagara+Kerrigan Commander)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'HydraliskFrenzy/Hydralisk', 'BurrowDown'], #Coop/Zerg/Units/Hydralisk
                   ['Drone/Larva', 'Overlord/Larva', 'Zergling/Larva', 'Aberration/Larva', 'Roach/Larva', 'Hydralisk/Larva', 'Infestor/Larva', 'Ultralisk/Larva', 'SwarmHostMP/Larva', 'Mutalisk/Larva', 'Brutalisk/Larva', 'Cancel', 'SwarmQueenZergling/SwarmQueenEgg', 'SwarmQueenRoach/SwarmQueenEgg', 'SwarmQueenHydralisk/SwarmQueenEgg', 'Cancel'], #Coop/Zerg/Units/Larva/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MorphToOverseer/Overlord', 'StopGenerateCreep/Overlord', 'BunkerLoad', 'BunkerUnloadAll', 'Cancel'], #Coop/Zerg/Units/Overlord/General (Creeping)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MorphtoOverseerSiege/Overseer', 'MorphtoOverseer/Overseer'], #Coop/Zerg/Units/Overseer
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'BuildCreepTumor/QueenCoop', 'MorphMorphalisk/QueenCoop', 'Transfusion/QueenCoop', 'BurrowDown'], #Coop/Zerg/Units/Queen
                   ['Attack', 'SetRallyPointSwarmHost/SwarmHostBurrowedMP', 'SwarmHost/SwarmHostBurrowedMP', 'SwarmHostBurrowUp'], #Coop/Zerg/Units/Swarm Host/Burrowed
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'BurrowChargeCampaign/Ultralisk', 'BurrowDown'], #Coop/Zerg/Units/Ultralisk
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'FaceEmbrace/Viper', 'DisablingCloud/Viper', 'ViperConsumption/Viper'], #Coop/Zerg/Units/Viper
                   ['Phoenix/StargateWarp', 'VoidRay/StargateWarp', 'Carrier/StargateWarp', 'MorphBackToStargate/StargateWarp', 'Cancel'], #LotV Campaign/Protoss Story/Structures/Warp Stargate
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'AlarakKnockback/AlarakChampion', 'AlarakDeadlyCharge/AlarakChampion', 'Rally'], #LotV Campaign/Protoss Story/Units/Alarak
                   ['ArtanisChannel/ArtanisVoid', 'ArtanisChannelOff/ArtanisVoid'], #LotV Campaign/Protoss Story/Units/Artanis/Extra
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'ArtanisLightningDash/ArtanisVoid', 'ArtanisAstralWind/ArtanisVoid', 'Rally'], #LotV Campaign/Protoss Story/Units/Artanis/Hero Zealot
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MassRecall/Artanis', 'Vortex/Artanis'], #LotV Campaign/Protoss Story/Units/Artanis/Mothership
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'FenixSOACharge/FenixChampion', 'FenixWhirlwind/FenixChampion', 'VoidShieldCapacitor/FenixChampion', 'Rally'], #LotV Campaign/Protoss Story/Units/Fenix/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'FenixSOACharge/FenixSOA', 'FenixWhirlwind/FenixSOA', 'Rally'], #LotV Campaign/Protoss Story/Units/Fenix/SOA Calldown
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Reclamation/KaraxChampion', 'PhaseCannon/KaraxChampion', 'Rally'], #LotV Campaign/Protoss Story/Units/Karax
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'VorazunBlink/VorazunChampion', 'MohandarOmnislash/VorazunChampion', 'Rally'], #LotV Campaign/Protoss Story/Units/Vorazun
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'ZeratulBlink/ZeratulVoidAiur01', 'PrologueVoidArmor/ZeratulVoidAiur01', 'ShadowBlade/ZeratulVoidAiur01', 'Rally'], #LotV Campaign/Protoss Story/Units/Zeratul/Aiur 01
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'ZeratulBlink/ZeratulVoid', 'ZeratulStun/ZeratulVoid', 'Rally'], #LotV Campaign/Protoss Story/Units/Zeratul/Void
                   ['ProtossAirWeaponsLevel1/CyberneticsCore', 'ProtossAirArmorLevel1/CyberneticsCore', 'ResearchHallucination/CyberneticsCore', 'ResearchWarpGate/CyberneticsCore', 'Cancel'], #LotV Campaign/Protoss/Structues/Cybernetics Core
                   ['Phoenix/Stargate', 'VoidRay/Stargate', 'Carrier/Stargate', 'Rally', 'UpgradeToStargateWarp/Stargate', 'Cancel'], #LotV Campaign/Protoss/Structues/Stargate
                   ['ResearchCharge/TwilightCouncil', 'ResearchStalkerTeleport/TwilightCouncil', 'WarpInVulcanChampion/TwilightCouncil', 'WarpInReaverChampion/TwilightCouncil', 'WarpInFenixChampion/TwilightCouncil', 'WarpInDarkArchonChampion/TwilightCouncil'], #LotV Campaign/Protoss/Structues/Twilight Council
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'BonesHeal/Stetmann'], #LotV Campaign/Terran Story/Units/Egon Stetmann
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MindBlast/Tosh', 'VoodooShield/Tosh', 'Consumption/Tosh', 'HeroNukeCalldown/Tosh'], #LotV Campaign/Terran Story/Units/Gabriel Tosh
                   ['MindControl/HiveMindEmulator', 'Cancel'], #LotV Campaign/Terran Story/Units/Hive Mind Emulator
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'SJHyperionFightersRecall/SJHyperion', 'SJHyperionBlink/SJHyperion', 'SJHyperionFighters/SJHyperion', 'SJHyperionYamato/SJHyperion', 'SJHyperionLightningStorm/SJHyperion'], #LotV Campaign/Terran Story/Units/Hyperion
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'PlantC4Charge/Raynor', 'TossGrenade/Raynor', 'ExperimentalPlasmaGun/Raynor', 'TheMorosDevice/Raynor'], #LotV Campaign/Terran Story/Units/Jim Raynor/Castanar
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'RaynorSnipe/RaynorCommando'], #LotV Campaign/Terran Story/Units/Jim Raynor/Char
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'NovaSnipe/Nova', 'Domination/Nova', 'ReleaseMinion/Nova', 'HeroNukeCalldown/Nova', 'Cancel'], #LotV Campaign/Terran Story/Units/Nova
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'DutchPlaceTurret/Swann'], #LotV Campaign/Terran Story/Units/Rory Swann
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'SpectreHoldFire/Spectre', 'SpectreWeaponsFree/Spectre', 'UltrasonicPulse/Spectre', 'Obliterate/Spectre', 'CloakOff', 'SpectreNukeCalldown/Spectre', 'Cancel'], #LotV Campaign/Terran Story/Units/Spectre/Cloaked
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'SpectreHoldFire/Spectre', 'SpectreWeaponsFree/Spectre', 'UltrasonicPulse/Spectre', 'Obliterate/Spectre', 'CloakOnBanshee', 'SpectreNukeCalldown/Spectre', 'Cancel'], #LotV Campaign/Terran Story/Units/Spectre/General
                   ['ResearchShieldWall/BarracksTechReactor', 'Stimpack/BarracksTechReactor', 'ReaperSpeed/BarracksTechReactor', 'Cancel'], #LotV Campaign/Terran Story/Units/Tech Reactor/Attached to Barracks
                   ['ResearchHighCapacityBarrels/FactoryTechReactor', 'ResearchSiegeTech/FactoryTechReactor', 'Cancel'], #LotV Campaign/Terran Story/Units/Tech Reactor/Attached to Factory
                   ['ResearchMedivacEnergyUpgrade/StarportTechReactor', 'ResearchBansheeCloak/StarportTechReactor', 'ResearchRavenEnergyUpgrade/StarportTechReactor', 'WraithCloak/StarportTechReactor', 'ResearchDurableMaterials/StarportTechReactor', 'ResearchSeekerMissile/StarportTechReactor', 'Cancel'], #LotV Campaign/Terran Story/Units/Tech Reactor/Attached to Starport
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'TossGrenadeTychus/TychusCommando'], #LotV Campaign/Terran Story/Units/Tychus Findlay
                   ['Hellion/Factory', 'Goliath/Factory', 'SiegeTank/Factory', 'Diamondback/Factory', 'Thor/Factory', 'MercHellion/Factory', 'HireSpartanCompany/Factory', 'HireSiegeBreakers/Factory', 'Cancel'], #LotV Campaign/Terran/Structures/Factory/AI Mess 02
                   ['Vulture/Factory', 'Hellion/Factory', 'SiegeTank/Factory', 'Diamondback/Factory', 'Goliath/Factory', 'Thor/Factory', 'CampaignVehicles/Factory', 'SelectBuilder', 'Rally', 'TechLabFactory/Factory', 'Reactor/Factory', 'Lift', 'Cancel'], #LotV Campaign/Terran/Structures/Factory/General
                   ['ResearchHighCapacityBarrels/FactoryTechLab', 'ResearchSiegeTech/FactoryTechLab', 'ResearchStrikeCannons/FactoryTechLab', 'Cancel'], #LotV Campaign/Terran/Structures/Tech Lab/Attached to Factory
                   ['ResearchMedivacEnergyUpgrade/StarportTechLab', 'ResearchDurableMaterials/StarportTechLab', 'ResearchSeekerMissile/StarportTechLab', 'ResearchRavenEnergyUpgrade/StarportTechLab', 'ResearchBansheeCloak/StarportTechLab', 'Cancel'], #LotV Campaign/Terran/Structures/Tech Lab/Attached to Starport
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'StukovBossBlast/InfestedStukov', 'DevastatingShot/InfestedStukov', 'StukovInfestedTerrans/InfestedStukov', 'StukovCrystalChannel/InfestedStukov'], #LotV Campaign/Zerg Story/Units/Alexei Stukov
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Explode/HotSHunter', 'DisableBuildingAttack/HotSHunter', 'BurrowDown'], #LotV Campaign/Zerg Story/Units/Baneling (Hunter Strain)/Enabled Building Attack
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Explode/HotSSplitterlingBig', 'DisableBuildingAttack/HotSSplitterlingBig', 'BurrowDown'], #LotV Campaign/Zerg Story/Units/Baneling (Splitter Strain)/Enabled Building Attack
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Explode/HotSSplitterlingBig', 'EnableBuildingAttack/HotSSplitterlingBig', 'BurrowDown'], #LotV Campaign/Zerg Story/Units/Baneling (Splitter Strain)/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Drag/Dehaka', 'DehakaMirrorImage/Dehaka', 'DehakaHeal/Dehaka', 'BurrowDown'], #LotV Campaign/Zerg Story/Units/Dehaka
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Drag/DehakaMirrorImage', 'BurrowDown'], #LotV Campaign/Zerg Story/Units/Dehaka Spawn
                   ['Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'ImpalerBurrowUp'], #LotV Campaign/Zerg Story/Units/Impaler/Burrowed
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'ImpalerBurrowDown'], #LotV Campaign/Zerg Story/Units/Impaler/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MindBolt/K5KerriganBurrowed', 'PsionicLift/K5KerriganBurrowed', 'WildMutation/K5KerriganBurrowed', 'K5Leviathan/K5KerriganBurrowed', 'BurrowUp'], #LotV Campaign/Zerg Story/Units/Kerrigan/Burrowed
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MindBolt/K5Kerrigan', 'PsionicLift/K5Kerrigan', 'WildMutation/K5Kerrigan', 'K5Leviathan/K5Kerrigan', 'BurrowDown'], #LotV Campaign/Zerg Story/Units/Kerrigan/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'KerriganEpilogue03QuantumRay/KerriganEpilogue03', 'KerriganEpilogue03Heal/KerriganEpilogue03', 'KerriganEpilogue03CreepTeleport/KerriganEpilogue03', 'KerriganEpilogue03Extinction/KerriganEpilogue03', 'Cancel'], #LotV Campaign/Zerg Story/Units/Kerrigan/Kerrigan - Empowered
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'KerriganVoidKineticBlast/KerriganVoidUlnar02', 'KerriganVoidSpawnBanelings/KerriganVoidUlnar02', 'KerriganVoidApocalypse/KerriganVoidUlnar02'], #LotV Campaign/Zerg Story/Units/Kerrigan/Kerrigan - Ulnar
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MindBolt/KerriganVoid', 'PsionicLift/KerriganVoid', 'WildMutation/KerriganVoid', 'K5Leviathan/KerriganVoid', 'Cancel'], #LotV Campaign/Zerg Story/Units/Kerrigan/Kerrigan - Void
                   ['MindBolt/KerriganVoidBurrowed', 'PsionicLift/KerriganVoidBurrowed', 'WildMutation/KerriganVoidBurrowed', 'K5Leviathan/KerriganVoidBurrowed', 'BurrowUp'], #LotV Campaign/Zerg Story/Units/Kerrigan/Kerrigan - Void - Burrowed
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MindBolt/KerriganGhostLab', 'PsionicLift/KerriganGhostLab'], #LotV Campaign/Zerg Story/Units/Kerrigan/Umoja Missions
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'ParasiticInvasion/LarvalQueen', 'GrowSwarmQueen/LarvalQueen'], #LotV Campaign/Zerg Story/Units/Niadra/Larva
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'SwarmQueenParasiticInvasion/SwarmQueen', 'SwarmQueenZergling/SwarmQueen', 'GrowLargeQueen/SwarmQueen', 'BurrowDown'], #LotV Campaign/Zerg Story/Units/Niadra/Stage 1
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'SwarmQueenParasiticInvasion/LargeSwarmQueen', 'SwarmQueenZergling/LargeSwarmQueen', 'SwarmQueenRoach/LargeSwarmQueen', 'GrowHugeQueen/LargeSwarmQueen', 'BurrowDown'], #LotV Campaign/Zerg Story/Units/Niadra/Stage 2
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'SwarmQueenParasiticInvasion/HugeSwarmQueen', 'SwarmQueenZergling/HugeSwarmQueen', 'SwarmQueenRoach/HugeSwarmQueen', 'SwarmQueenHydralisk/HugeSwarmQueen', 'BurrowDown'], #LotV Campaign/Zerg Story/Units/Niadra/Stage 3
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'QueenClassicParasite/QueenClassic', 'QueenMPEnsnare/QueenClassic', 'QueenMPSpawnBroodlings/QueenClassic', 'CreepTumor/QueenClassic'], #LotV Campaign/Zerg Story/Units/Queen
                   ['Larva', 'Queen', 'ResearchBurrow', 'overlordspeed', 'EvolveVentralSacks', 'RallyEgg', 'Rally', 'Lair/Hatchery', 'Cancel'], #LotV Campaign/Zerg/Structures/Hatchery
                   ['Larva', 'Queen', 'RespawnZergling/Hive', 'overlordspeed', 'EvolveVentralSacks', 'RallyEgg', 'Rally', 'Cancel'], #LotV Campaign/Zerg/Structures/Hive
                   ['hydraliskspeed/HydraliskDen', 'LurkerDen/HydraliskDen', 'Cancel'], #LotV Campaign/Zerg/Structures/Hydralisk Den
                   ['Larva', 'Queen', 'ResearchBurrow', 'overlordspeed', 'EvolveVentralSacks', 'RallyEgg', 'Rally', 'Hive/Lair', 'Cancel'], #LotV Campaign/Zerg/Structures/Lair
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'FungalGrowth/Infestor', 'InfestedTerrans/Infestor', 'InfestorConsumption/Infestor', 'Cancel', 'BurrowDown'], #LotV Campaign/Zerg/Units/Infestor/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'BuildCreepTumor/Queen', 'QueenBurstHeal/Queen', 'MorphMorphalisk/Queen', 'DeepTunnel/Queen', 'BurrowDown'], #LotV Campaign/Zerg/Units/Queen
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Interceptor/Selendis', 'Cancel'], #LotV Prologue/Protoss Story/Units/Selendis (WoL Protoss Missions)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'GravitonBeam/Urun', 'Rally'], #LotV Prologue/Protoss Story/Units/Urun (WoL Protoss Missions)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'ZeratulBlink/PrologueZeratul', 'PrologueVoidArmor/PrologueZeratul', 'ShadowBlade/PrologueZeratul', 'Rally'], #LotV Prologue/Protoss Story/Units/Zeratul (LotV Prologue)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'ZeratulBlink/Zeratul', 'ZeratulStun/Zeratul', 'Rally'], #LotV Prologue/Protoss Story/Units/Zeratul (WoL Protoss Missions)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MassRecall/Mothership', 'Vortex/Mothership'], #LotV Prologue/Protoss/Units/Mothership
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'VoidSiphon/Oracle', 'OracleRevelation/Oracle', 'ResourceStun/Oracle', 'Cancel'], #LotV Prologue/Protoss/Units/Oracle
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'GatherProt', 'ReturnCargo', 'GasCanisterGather/Probe', 'ProtossBuild/Probe', 'ProtossBuildAdvanced/Probe'], #LotV Prologue/Protoss/Units/Probe/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Blink/ShadowOfTheVoidStalker', 'Rally'], #LotV Prologue/Protoss/Units/Shadow of the Void (Stalker)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Charge/ShadowOfTheVoidZealot', 'Rally'], #LotV Prologue/Protoss/Units/Shadow of the Void (Zealot)
                   ['HireKelmorianMiners/MercCompound', 'HireDevilDogs/MercCompound', 'HireHammerSecurities/MercCompound', 'HireSpartanCompany/MercCompound', 'HireSiegeBreakers/MercCompound', 'HireHelsAngels/MercCompound', 'HireDuskWing/MercCompound', 'HireDukesRevenge/MercCompound', 'MercMedic/MercCompound', 'ReaperSpeed/MercCompound', 'MercHellion/MercCompound', 'MercReaper/MercCompound', 'Rally', 'Halt', 'Cancel'], #LotV Prologue/Terran Story/Units/Merc Compound
                   ['TerranVehicleWeaponsLevel1/Armory', 'TerranVehiclePlatingLevel1/Armory', 'TerranShipWeaponsLevel1/Armory', 'TerranShipPlatingLevel1/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #LotV Prologue/Terran/Structures/Armory
                   ['Marine/Barracks', 'Marauder/Barracks', 'Reaper/Barracks', 'Ghost/Barracks', 'Medic/Barracks', 'Firebat/Barracks', 'Spectre/Barracks', 'SelectBuilder', 'Rally', 'TechLabBarracks/Barracks', 'Reactor/Barracks', 'TechReactorAI/Barracks', 'Lift', 'Cancel'], #LotV Prologue/Terran/Structures/Barracks/General
                   ['Vulture/Factory', 'Predator/Factory', 'Diamondback/Factory', 'Goliath/Factory', 'MicroBot/Factory', 'Thor/Factory', 'Hellion/Factory', 'Cancel'], #LotV Prologue/Terran/Structures/Factory/AI Mess 01
                   ['Hellion/Factory', 'SiegeTank/Factory', 'WarHound/Factory', 'CampaignVehicles/Factory', 'SelectBuilder', 'Rally', 'TechLabFactory/Factory', 'Reactor/Factory', 'TechReactorAI/Factory', 'Lift', 'Cancel'], #LotV Prologue/Terran/Structures/Factory/General
                   ['VikingFighter/Starport', 'Medivac/Starport', 'Raven/Starport', 'Banshee/Starport', 'Battlecruiser/Starport', 'CampaignVehicles/Starport', 'SelectBuilder', 'Rally', 'TechLabStarport/Starport', 'Reactor/Starport', 'TechReactorAI/Starport', 'Lift', 'Cancel'], #LotV Prologue/Terran/Structures/Starport/General
                   ['ResearchShieldWall/BarracksTechLab', 'Stimpack/BarracksTechLab', 'ResearchPunisherGrenades/BarracksTechLab', 'ReaperSpeed/BarracksTechLab', 'Cancel'], #LotV Prologue/Terran/Structures/Tech Lab/Attached to Barracks
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'TornadoMissile/WarHound'], #LotV Prologue/Terran/Units/Warhound
                   ['Larva', 'Queen', 'RespawnZergling/Hatchery', 'overlordspeed', 'EvolveVentralSacks', 'RallyEgg', 'Rally', 'Lair/Hatchery', 'Cancel'], #LotV Prologue/Zerg/Structures/Hatchery
                   ['Larva', 'Queen', 'RespawnZergling/Lair', 'overlordspeed', 'EvolveVentralSacks', 'RallyEgg', 'Rally', 'Hive/Lair', 'Cancel'], #LotV Prologue/Zerg/Structures/Lair
                   ['ResearchInterceptorLaunchSpeedUpgrade/FleetBeacon', 'OracleEnergyUpgrade/FleetBeacon', 'TempestRangeUpgrade/FleetBeacon', 'Cancel'], #HotS Campaign/Protoss/Units/Fleet Beacon
                   ['Phoenix/Stargate', 'VoidRay/Stargate', 'Carrier/Stargate', 'Oracle/Stargate', 'Tempest/Stargate', 'WarpInScout/Stargate', 'Rally', 'Cancel'], #HotS Campaign/Protoss/Units/Stargate
                   ['Marine/Barracks', 'Marauder/Barracks', 'Reaper/Barracks', 'Ghost/Barracks', 'Medic/Barracks', 'Firebat/Barracks', 'Spectre/Barracks', 'MengskUnits/Barracks', 'Rally', 'TechLabBarracks/Barracks', 'Reactor/Barracks', 'TechReactorAI/Barracks', 'Lift', 'Cancel'], #HotS Campaign/Terran/Structures/Barracks/General (non-constructing)
                   ['Hellion/Factory', 'SiegeTank/Factory', 'WarHound/Factory', 'CampaignVehicles/Factory', 'MengskUnits/Factory', 'Rally', 'TechLabFactory/Factory', 'Reactor/Factory', 'TechReactorAI/Factory', 'Lift', 'Cancel'], #HotS Campaign/Terran/Structures/Factory/General (non-constructing)
                   ['VikingFighter/Starport', 'Medivac/Starport', 'Raven/Starport', 'Banshee/Starport', 'Battlecruiser/Starport', 'CampaignVehicles', 'SelectBuilder', 'Rally', 'TechLabStarport/Starport', 'Reactor/Starport', 'TechReactorAI/Starport', 'Lift', 'Cancel'], #HotS Campaign/Terran/Structures/Starport/General
                   ['VikingFighter/Starport', 'Medivac/Starport', 'Raven/Starport', 'Banshee/Starport', 'Battlecruiser/Starport', 'CampaignVehicles', 'MengskUnits/Starport', 'Rally', 'TechLabStarport/Starport', 'Reactor/Starport', 'TechReactorAI/Starport', 'Lift', 'Cancel'], #HotS Campaign/Terran/Structures/Starport/General (non-constructing)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Consume/GiantYeti', 'GiantYetiLeap/GiantYeti'], #HotS Campaign/Zerg Story/Units/Giant Ursadon (Enemy Within Mission)
                   ['Stop', 'Consume/Lyote'], #HotS Campaign/Zerg Story/Units/Lyote (Enemy Within Mission)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Explode/HotSSplitterlingBig', 'DisableBuildingAttackSplitterling/HotSSplitterlingBig', 'BurrowDown'], #HotS Campaign/Zerg/Units/Baneling (Splitter Strain,split)/Enabled Building Attack
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Explode/HotSSplitterlingBig', 'EnableBuildingAttackSplitterling/HotSSplitterlingBig', 'BurrowDown'], #HotS Campaign/Zerg/Units/Baneling (Splitter Strain,split)/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'FungalGrowth/Infestor', 'NPSwarm/Infestor', 'InfestorConsumption/Infestor', 'BurrowDown'], #HotS Campaign/Zerg/Units/Infestor
                   ['Stop', 'Attack', 'LocustFlyingLaunch/SwarmHostSplitABurrowed', 'RapidIncubation/SwarmHostSplitBBurrowed', 'SwarmHostUprootUnburrow'], #HotS Campaign/Zerg/Units/Swarm Host (Carrion Strain)/Burrowed
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'RapidIncubation/SwarmHostSplitA', 'SwarmHostRootBurrow'], #HotS Campaign/Zerg/Units/Swarm Host (Carrion Strain)/General (Burrow)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'RapidIncubation/SwarmHostSplitA', 'SwarmHostRoot'], #HotS Campaign/Zerg/Units/Swarm Host (Carrion Strain)/General (Rapid Incubation)
                   ['Stop', 'Attack', 'LocustFlyingLaunch/SwarmHostSplitARooted', 'RapidIncubation/SwarmHostSplitARooted', 'SwarmHostUproot'], #HotS Campaign/Zerg/Units/Swarm Host (Carrion Strain)/Rooted (Rapid Incubation)
                   ['Stop', 'Attack', 'LocustLaunchCreeper/SwarmHostSplitBBurrowed', 'SwarmHostDeepBurrow/SwarmHostSplitBBurrowed', 'RapidIncubation/SwarmHostSplitBBurrowed', 'SwarmHostUprootUnburrow'], #HotS Campaign/Zerg/Units/Swarm Host (Creeper Strain)/Burrowed
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'SwarmHostDeepBurrow/SwarmHostSplitB', 'RapidIncubation/SwarmHostSplitB', 'SwarmHostRootBurrow'], #HotS Campaign/Zerg/Units/Swarm Host (Creeper Strain)/General (Burrow)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'SwarmHostDeepBurrow/SwarmHostSplitB', 'RapidIncubation/SwarmHostSplitB', 'SwarmHostRoot'], #HotS Campaign/Zerg/Units/Swarm Host (Creeper Strain)/General (Rapid Incubation)
                   ['Stop', 'Attack', 'LocustLaunchCreeper/SwarmHostSplitBRooted', 'SwarmHostDeepBurrow/SwarmHostSplitBRooted', 'RapidIncubation/SwarmHostSplitBRooted', 'SwarmHostUproot'], #HotS Campaign/Zerg/Units/Swarm Host (Creeper Strain)/Rooted (Rapid Incubation)
                   ['Stop', 'Attack', 'LocustLaunch/SwarmHostBurrowed', 'RapidIncubation/SwarmHostBurrowed', 'SwarmHostUprootUnburrow'], #HotS Campaign/Zerg/Units/Swarm Host/Burrowed
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'RapidIncubation/SwarmHost', 'SwarmHostRootBurrow'], #HotS Campaign/Zerg/Units/Swarm Host/General (Burrow)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'RapidIncubation/SwarmHost', 'SwarmHostRoot'], #HotS Campaign/Zerg/Units/Swarm Host/General (Rapid Incubation)
                   ['Stop', 'Attack', 'LocustLaunch/SwarmHostRooted', 'RapidIncubation/SwarmHostRooted', 'SwarmHostUproot'], #HotS Campaign/Zerg/Units/Swarm Host/Rooted (Rapid Incubation)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'TorrasqueChrysalis/HotSTorrasqueBurrowed', 'BurrowUp'], #HotS Campaign/Zerg/Units/Ultralisk (Torrasque)/Burrowed
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'BurrowChargeCampaign/HotSTorrasque', 'TorrasqueChrysalis/HotSTorrasque', 'BurrowDown'], #HotS Campaign/Zerg/Units/Ultralisk (Torrasque)/General
                   ['ResearchVoidRaySpeedUpgrade/FleetBeacon', 'ResearchInterceptorLaunchSpeedUpgrade/FleetBeacon', 'Cancel'], #WoL Campaign/Protoss/Structues/Fleet Beacon
                   ['HireKelmorianMiners/MercCompound', 'HireDevilDogs/MercCompound', 'HireHammerSecurities/MercCompound', 'HireSpartanCompany/MercCompound', 'HireSiegeBreakers/MercCompound', 'HireHelsAngels/MercCompound', 'HireDuskWing/MercCompound', 'SelectBuilder', 'Rally', 'HireDukesRevenge/MercCompound', 'Halt', 'Cancel'], #WoL Campaign/Terran Story/Structues/Merc Compound
                   ['SelectBuilder', 'SpectreNukeArm/GhostAcademy', 'Halt', 'Cancel'], #WoL Campaign/Terran Story/Structues/Shadow Ops
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'YamatoGun', 'MissilePods/DukesRevenge', 'DefensiveMatrix/DukesRevenge'], #WoL Campaign/Terran Story/Units/Jackson's Revenge
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'OdinBarrage/Odin', 'OdinNukeCalldown/Odin', 'Cancel'], #WoL Campaign/Terran Story/Units/Odin
                   ['TerranVehicleWeaponsUltraCapacitorsLevel1/Armory', 'TerranVehiclePlatingLevel1/Armory', 'TerranShipWeaponsUltraCapacitorsLevel1/Armory', 'TerranShipPlatingLevel1/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Armory/Ultra Capacitors, Vehicle/Ship: 1/1
                   ['TerranVehicleWeaponsUltraCapacitorsLevel1/Armory', 'TerranVehiclePlatingLevel1/Armory', 'TerranShipWeaponsUltraCapacitorsLevel2/Armory', 'TerranShipPlatingLevel1/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Armory/Ultra Capacitors, Vehicle/Ship: 1/2
                   ['TerranVehicleWeaponsUltraCapacitorsLevel1/Armory', 'TerranVehiclePlatingLevel1/Armory', 'TerranShipWeaponsUltraCapacitorsLevel3/Armory', 'TerranShipPlatingLevel1/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Armory/Ultra Capacitors, Vehicle/Ship: 1/3
                   ['TerranVehicleWeaponsUltraCapacitorsLevel2/Armory', 'TerranVehiclePlatingLevel1/Armory', 'TerranShipWeaponsUltraCapacitorsLevel1/Armory', 'TerranShipPlatingLevel1/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Armory/Ultra Capacitors, Vehicle/Ship: 2/1
                   ['TerranVehicleWeaponsUltraCapacitorsLevel2/Armory', 'TerranVehiclePlatingLevel1/Armory', 'TerranShipWeaponsUltraCapacitorsLevel2/Armory', 'TerranShipPlatingLevel1/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Armory/Ultra Capacitors, Vehicle/Ship: 2/2
                   ['TerranVehicleWeaponsUltraCapacitorsLevel2/Armory', 'TerranVehiclePlatingLevel1/Armory', 'TerranShipWeaponsUltraCapacitorsLevel3/Armory', 'TerranShipPlatingLevel1/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Armory/Ultra Capacitors, Vehicle/Ship: 2/3
                   ['TerranVehicleWeaponsUltraCapacitorsLevel3/Armory', 'TerranVehiclePlatingLevel1/Armory', 'TerranShipWeaponsUltraCapacitorsLevel1/Armory', 'TerranShipPlatingLevel1/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Armory/Ultra Capacitors, Vehicle/Ship: 3/1
                   ['TerranVehicleWeaponsUltraCapacitorsLevel3/Armory', 'TerranVehiclePlatingLevel1/Armory', 'TerranShipWeaponsUltraCapacitorsLevel2/Armory', 'TerranShipPlatingLevel1/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Armory/Ultra Capacitors, Vehicle/Ship: 3/2
                   ['TerranVehicleWeaponsUltraCapacitorsLevel3/Armory', 'TerranVehiclePlatingLevel1/Armory', 'TerranShipWeaponsUltraCapacitorsLevel3/Armory', 'TerranShipPlatingLevel1/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Armory/Ultra Capacitors, Vehicle/Ship: 3/3
                   ['TerranVehicleWeaponsLevel1/Armory', 'TerranVehiclePlatingVanadiumPlatingLevel1/Armory', 'TerranShipWeaponsLevel1/Armory', 'TerranShipPlatingVanadiumPlatingLevel1/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Armory/Vanadium Plating, Vehicle/Ship: 1/1
                   ['TerranVehicleWeaponsLevel1/Armory', 'TerranVehiclePlatingVanadiumPlatingLevel1/Armory', 'TerranShipWeaponsLevel1/Armory', 'TerranShipPlatingVanadiumPlatingLevel2/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Armory/Vanadium Plating, Vehicle/Ship: 1/2
                   ['TerranVehicleWeaponsLevel1/Armory', 'TerranVehiclePlatingVanadiumPlatingLevel1/Armory', 'TerranShipWeaponsLevel1/Armory', 'TerranShipPlatingVanadiumPlatingLevel3/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Armory/Vanadium Plating, Vehicle/Ship: 1/3
                   ['TerranVehicleWeaponsLevel1/Armory', 'TerranVehiclePlatingVanadiumPlatingLevel2/Armory', 'TerranShipWeaponsLevel1/Armory', 'TerranShipPlatingVanadiumPlatingLevel1/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Armory/Vanadium Plating, Vehicle/Ship: 2/1
                   ['TerranVehicleWeaponsLevel1/Armory', 'TerranVehiclePlatingVanadiumPlatingLevel2/Armory', 'TerranShipWeaponsLevel1/Armory', 'TerranShipPlatingVanadiumPlatingLevel2/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Armory/Vanadium Plating, Vehicle/Ship: 2/2
                   ['TerranVehicleWeaponsLevel1/Armory', 'TerranVehiclePlatingVanadiumPlatingLevel2/Armory', 'TerranShipWeaponsLevel1/Armory', 'TerranShipPlatingVanadiumPlatingLevel3/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Armory/Vanadium Plating, Vehicle/Ship: 2/3
                   ['TerranVehicleWeaponsLevel1/Armory', 'TerranVehiclePlatingVanadiumPlatingLevel3/Armory', 'TerranShipWeaponsLevel1/Armory', 'TerranShipPlatingVanadiumPlatingLevel1/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Armory/Vanadium Plating, Vehicle/Ship: 3/1
                   ['TerranVehicleWeaponsLevel1/Armory', 'TerranVehiclePlatingVanadiumPlatingLevel3/Armory', 'TerranShipWeaponsLevel1/Armory', 'TerranShipPlatingVanadiumPlatingLevel2/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Armory/Vanadium Plating, Vehicle/Ship: 3/2
                   ['TerranVehicleWeaponsLevel1/Armory', 'TerranVehiclePlatingVanadiumPlatingLevel3/Armory', 'TerranShipWeaponsLevel1/Armory', 'TerranShipPlatingVanadiumPlatingLevel3/Armory', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Armory/Vanadium Plating, Vehicle/Ship: 3/3
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'TechReactor/BarracksFlying', 'Land'], #WoL Campaign/Terran/Structures/Barracks/Flying (Tech Reactor)
                   ['SCV', 'UpgradeToPlanetaryFortress/CommandCenter', 'Scan/CommandCenter', 'CalldownMULE/CommandCenter', 'SelectBuilder', 'Rally', 'CommandCenterLoad', 'CommandCenterUnloadAll', 'Lift', 'Cancel'], #WoL Campaign/Terran/Structures/Command Center/General (Orbital Relay)
                   ['TerranInfantryWeaponsUltraCapacitorsLevel1/EngineeringBay', 'TerranInfantryArmorLevel1/EngineeringBay', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Engineering Bay/Ultra Capacitors level 1
                   ['TerranInfantryWeaponsUltraCapacitorsLevel2/EngineeringBay', 'TerranInfantryArmorLevel1/EngineeringBay', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Engineering Bay/Ultra Capacitors level 2
                   ['TerranInfantryWeaponsUltraCapacitorsLevel3/EngineeringBay', 'TerranInfantryArmorLevel1/EngineeringBay', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Engineering Bay/Ultra Capacitors level 3
                   ['TerranInfantryWeaponsLevel1/EngineeringBay', 'TerranInfantryArmorVanadiumPlatingLevel1/EngineeringBay', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Engineering Bay/Vanadium Plating level 1
                   ['TerranInfantryWeaponsLevel1/EngineeringBay', 'TerranInfantryArmorVanadiumPlatingLevel2/EngineeringBay', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Engineering Bay/Vanadium Plating level 2
                   ['TerranInfantryWeaponsLevel1/EngineeringBay', 'TerranInfantryArmorVanadiumPlatingLevel3/EngineeringBay', 'SelectBuilder', 'Halt', 'Cancel'], #WoL Campaign/Terran/Structures/Engineering Bay/Vanadium Plating level 3
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'TechReactor/FactoryFlying', 'Land'], #WoL Campaign/Terran/Structures/Factory/Flying (Tech Reactor)
                   ['Hellion/Factory', 'SiegeTank/Factory', 'Thor/Factory', 'Predator/Factory', 'Vulture/Factory', 'Diamondback/Factory', 'Goliath/Factory', 'SelectBuilder', 'Rally', 'TechLabFactory/Factory', 'Reactor/Factory', 'TechReactorAI/Factory', 'Lift', 'Cancel'], #WoL Campaign/Terran/Structures/Factory/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'TechReactor/StarportFlying', 'Land'], #WoL Campaign/Terran/Structures/Starport/Flying (Tech Reactor)
                   ['VikingFighter/Starport', 'Medivac/Starport', 'Raven/Starport', 'Banshee/Starport', 'Battlecruiser/Starport', 'Wraith/Starport', 'BuildHercules/Starport', 'SelectBuilder', 'Rally', 'TechLabStarport/Starport', 'Reactor/Starport', 'TechReactorAI/Starport', 'Lift', 'Cancel'], #WoL Campaign/Terran/Structures/Starport/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'YamatoGun', 'MissilePods/Battlecruiser', 'DefensiveMatrix/Battlecruiser'], #WoL Campaign/Terran/Units/Battlecruiser
                   ['CommandCenter/SCV', 'Refinery/SCV', 'SupplyDepot/SCV', 'Barracks/SCV', 'EngineeringBay/SCV', 'PerditionTurret/SCV', 'Bunker/SCV', 'MissileTurret/SCV', 'SensorTower/SCV', 'HiveMindEmulator/SCV', 'Cancel'], #WoL Campaign/Terran/Units/SCV/Basic Structures
                   ['CommandCenterOrbRelay/SCV', 'Refinery/SCV', 'SupplyDepot/SCV', 'Barracks/SCV', 'EngineeringBay/SCV', 'PerditionTurret/SCV', 'Bunker/SCV', 'MissileTurret/SCV', 'SensorTower/SCV', 'HiveMindEmulator/SCV', 'Cancel'], #WoL Campaign/Terran/Units/SCV/Basic Structures (Orbital Relay purchased)
                   ['EvolvePeristalsis/InfestationPit', 'EvolveInfestorEnergyUpgrade/InfestationPit', 'Cancel'], #WoL Campaign/Zerg/Structures/Infestation Pit
                   ['EvolveAnabolicSynthesis2/UltraliskCavern', 'EvolveChitinousPlating/UltraliskCavern', 'Cancel'], #WoL Campaign/Zerg/Structures/Ultralisk Cavern
                   ['Drone/Larva', 'Overlord/Larva', 'Zergling/Larva', 'Roach/Larva', 'Hydralisk/Larva', 'Infestor/Larva', 'Scourge/Larva', 'Ultralisk/Larva', 'SwarmHostMP/Larva', 'Mutalisk/Larva', 'Cancel'], #WoL Campaign/Zerg/Units/Larva/General
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'OracleRevelation/Oracle', 'LightofAiur/Oracle', 'OracleWeaponOn/Oracle', 'OracleWeaponOff/Oracle', 'Cancel'], #HotS Multiplayer/Protoss/Units/Oracle
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'ArmorpiercingMode', 'ExplosiveMode', 'Cancel'], #HotS Multiplayer/Terran/Units/Thor
                   ['hydraliskspeed/HydraliskDen', 'MuscularAugments/HydraliskDen', 'Cancel'], #HotS Multiplayer/Zerg/Structures/Hydralisk Den
                   ['EvolveInfestorEnergyUpgrade/InfestationPit', 'ResearchNeuralParasite/InfestationPit', 'EvolveFlyingLocusts/InfestationPit', 'Cancel'], #HotS Multiplayer/Zerg/Structures/Infestation Pit
                   ['ResearchMedic/ScienceFacility', 'ResearchFirebat/ScienceFacility', 'ResearchReaper/ScienceFacility', 'ResearchHellion/ScienceFacility', 'ResearchGoliath/ScienceFacility', 'ResearchSiegeTank/ScienceFacility', 'ResearchBunkerUpgrade/ScienceFacility', 'ResearchPerditionTurret/ScienceFacility', 'ResearchFireSuppression/ScienceFacility', 'ResearchTechReactor/ScienceFacility'], #Left2Die/Terran Story/Structures/Science Facility
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'D8Charge/MercReaper'], #Left2Die/Terran Story/Units/Death Head (Reaper Merc)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'IncineratorNozzles/DevilDog', 'StimFirebat/DevilDog'], #Left2Die/Terran Story/Units/Devil Dog (Firebat Merc)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'IncineratorNozzles/Firebat', 'StimFirebat/Firebat'], #Left2Die/Terran Story/Units/Firebat
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Stim', 'JackhammerConcussionGrenade/HammerSecurity'], #Left2Die/Terran Story/Units/Hammer Securities (Marauder Merc)
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'MercMedicHeal/MercMedic'], #Left2Die/Terran Story/Units/Skibi's Angels (Merc Medic)
                   ['Stimpack/BarracksTechLab', 'ResearchJackhammerConcussionGrenade/BarracksTechLab', 'ResearchStabilizerMedPacks/BarracksTechLab', 'ResearchIncineratorNozzles/BarracksTechLab', 'ResearchG4Charge/BarracksTechLab', 'Cancel'], #Left2Die/Terran/Structures/Tech Lab/Attached to Barracks
                   ['ResearchCerberusMines/FactoryTechLab', 'ResearchHighCapacityBarrels/FactoryTechLab', 'ResearchMultiLockTargetingSystem/FactoryTechLab', 'ResearchShapedBlast/FactoryTechLab', 'ResearchRegenerativeBioSteel/FactoryTechLab', 'Cancel'], #Left2Die/Terran/Structures/Tech Lab/Attached to Factory
                   ['Move', 'Stop', 'MoveHoldPosition', 'MovePatrol', 'Attack', 'Stim', 'JackhammerConcussionGrenade/Marauder']] #Left2Die/Terran/Units/Marauder


# Read the settings
settings_parser = SafeConfigParser()
settings_parser.optionxform = str
settings_parser.read('MapDefinitions.ini')

I18N_parser = SafeConfigParser()
I18N_parser.optionxform = str
I18N_parser.read('KeyboardLayouts.ini')

race_dict = {"P": 0,
             "T": 1,
             "Z": 2,
             "R": 3}

prefix = settings_parser.get("Filenames", "Prefix")
suffix = settings_parser.get("Filenames", "Suffix")
Seed_files_folder = settings_parser.get("Filenames", "Seed_files_folder")
races = ["P", "T", "R", "Z"]
layouts = ["RM"]
layoutIndices = {"LMM": 0,
                 "RMM": 1,
                 "RM": 2}
righty_index = {0: False,
                1: True,
                2: True}


class Hotkey:
    def __init__(self, name, section, P=None, T=None, Z=None, R=None, default=None, copyOf=None):
        self.name = name
        self.section = section
        self.P = P
        self.T = T
        self.Z = Z
        self.R = R
        self.default = default
        self.copyOf = copyOf

    def set_value(self, race, value):
        if race == "P":
            self.P = value
        elif race == "R":
            self.R = value
        elif race == "T":
            self.T = value
        elif race == "Z":
            self.Z = value

    def get_value(self, race):
        if race == "P":
            return self.P
        elif race == "R":
            return self.R
        elif race == "T":
            return self.T
        elif race == "Z":
            return self.Z

def verify_file(filepath):
    print("verify file: " + filepath)
    hotkeys_file = open(filepath, 'r')
    dict = {}
    for line in hotkeys_file:
        line = line.strip()
        if len(line) == 0 or line[0] == "[":
            continue
        pair = line.split("=")
        key = pair[0]
        if key in dict:
            dict[key] = [True, pair[1], key, dict[key][3]]
        else:
            dict[key] = [True, pair[1], key, ""]

    # Check for duplicates
    if SHOW_DUPLICATES:
        verify_parser = SafeConfigParser()
        verify_parser.optionxform = str
        dup_dict = {}
        verify_parser.read(filepath)
        gen_items = verify_parser.items('Hotkeys')
        for pair in gen_items:
            if pair[1] in dup_dict:
                dup_dict[pair[1]].append(pair[0])
            else:
                dup_dict[pair[1]] = [pair[0]]
        for key in dup_dict:
            array = dup_dict[key]
            if len(array) > 1:
                print("============================")
                print(key + "    DUPLICATES")
                for a in array:
                    print(a)

    for same_set in SAME_CHECKS:
        mismatched = False
        value = dict[same_set[0]][1]
        for item in same_set:
            if not dict[item][1] == value:
                mismatched = True
        if mismatched:
            print("============================")
            print("---- Mismatched values ----")
            for item in same_set:
                print(item + " = " + dict[item][1])

    for conflict_set in CONFLICT_CHECKS:
        hotkeys = []
        count_hotkeys = {}
        for item in conflict_set:
            if not dict.__contains__(item):
                print('WARNING: ' + item + ' does not exist in HotKey-file')
            else :
                append = dict[item][1]
                hotkeys.append(append)
        for key in hotkeys:
            if not key in count_hotkeys:
                count_hotkeys[key] = 1
            else:
                count_hotkeys[key] = count_hotkeys[key] + 1
        for count in count_hotkeys:
            if count_hotkeys[count] > 1:
                print("============================")
                print("---- Conflict of hotkeys ----")
                for item in conflict_set:
                    key = dict[item][1]
                    if count_hotkeys[key] > 1:
                        print(item + " = " + key)
                # print(conflict_set)
    print("")

def parse_pair(parser, key, values, map_name, index, altgr):
    parsed = ""
    first = True
    for value in values:
        bits = value.split("+")
        if not first:
            parsed += ","
        if bits[0] == "Alt" and altgr == 1:
            bits[0] = "Control+Alt"
        last_bit = bits[len(bits) - 1]
        try:
            if index < 0:
                bits[len(bits) - 1] = parser.get(map_name, last_bit)
            else:
                bits[len(bits) - 1] = parser.get(map_name, last_bit).split(",")[index]
        except:
            last_bit = last_bit  # Do nothing
        # if is_rl_shift and "|" in bits[len(bits)-1]:
        #    try:
        #        unused = parser.get("MappingTypes", key).split(",")
        #        bits[len(bits)-1] = bits[len(bits)-1].split("|")[0]
        #    except:
        #        bits[len(bits)-1] = bits[len(bits)-1].split("|")[1]
        #    if not bits[len(bits)-1] == "":
        #        parsed += "+".join(bits)
        if not bits[len(bits) - 1] == "":
            parsed += "+".join(bits)

        first = False
    return parsed

def generate_layout(filename, race, layout, layoutIndex):
    filepath = Seed_files_folder + "/" + filename
    hotkeys_file = open(filepath, 'r')
    output = ""
    for line in hotkeys_file:
        line = line.strip()
        if len(line) == 0 or line[0] == "[":
            output += line + "\n"
            continue
        pair = line.split("=")
        key = pair[0]
        values = pair[1].split(",")
        output += key + "="

        # No need to distinguish between map types anymore. Just use GlobalMaps
        if key in EXCLUDE_MAPPING:
            output += pair[1]
        else:
            try:
                output += parse_pair(settings_parser, key, values, 'GlobalMaps', GLOBAL, 0)
            except:
                output += pair[1]

        # if key in CAMERA_KEYS:
            # if "R" in layout:
                # output += parse_pair(settings_parser, key, values, 'GlobalMaps', GLOBAL, 0)
            # else:
                # output += pair[1]
        # #elif race == "Z" and "MM" in layout and key in ZERG_CONTROL_GROUP_SPECIAL:
        # #    output += parse_pair(settings_parser, key, values, race + 'SCGMaps', layoutIndex, 0)
        # elif key in CONTROL_GROUP_KEYS:
            # output += parse_pair(settings_parser, key, values, race + 'CGMaps', layoutIndex, 0)
        # elif key in GENERAL_KEYS:
            # if "R" in layout:
                # output += parse_pair(settings_parser, key, values, 'GlobalMaps', GLOBAL, 0)
            # else:
                # output += pair[1]
        # else:
            # try:
                # #maptypes = settings_parser.get("MappingTypes", key).split(",")
                # maptypes = ["A","A","A","A"] # Only use ability maps
                # output += parse_pair(settings_parser, key, values, race + maptypes[race_dict[race]] + "Maps", layoutIndex, 0)
            # except:
                # output += pair[1]
        output += "\n"
    hotkeys_file.close()
    newfilename = filename.replace("LM", layout)
    newfilepath = Seed_files_folder + "/" + newfilename
    fileio = open(newfilepath, 'w')
    fileio.write(output)
    fileio.close()
    if VERIFY_ALL:
        verify_file(newfilepath)
    return newfilename

def shift_hand_size(filename, shift_right, hand_size, is_righty):
    filepath = Seed_files_folder + "/" + filename
    hotkeys_file = open(filepath, 'r')
    output = ""
    if is_righty:
        map_prefix = "R"
    else:
        map_prefix = "L"
    for line in hotkeys_file:
        line = line.strip()
        if len(line) == 0 or line[0] == "[":
            output += line + "\n"
            continue
        pair = line.split("=")
        key = pair[0]
        values = pair[1].split(",")
        output += key + "="

        if key in EXCLUDE_MAPPING:
            output += pair[1]
        elif shift_right:
            output += parse_pair(settings_parser, key, values, map_prefix + 'ShiftRightMaps', GLOBAL, 0)
        else:
            output += parse_pair(settings_parser, key, values, map_prefix + 'ShiftLeftMaps', GLOBAL, 0)
        output += "\n"
    hotkeys_file.close()
    newfilename = ""
    if "MM " in filename:
        newfilename = filename.replace("MM ", hand_size + "M ")
    else:
        newfilename = filename.replace("M ", hand_size + " ")
    newfilepath = Seed_files_folder + "/" + newfilename
    fileio = open(newfilepath, 'w')
    fileio.write(output)
    fileio.close()
    if VERIFY_ALL:
        verify_file(newfilepath)
    return newfilename

def translate_file(filename, is_righty):
    if not TRANSLATE:
        return
    seed_filepath = Seed_files_folder + "/" + filename
    layouts = I18N_parser.sections()
    for layout_name in layouts:
        hotkeys_file = open(seed_filepath, 'r')
        output = ""
        if is_righty:
            altgr = int(I18N_parser.get(layout_name, "AltGr"))
        else:
            altgr = 0

        for line in hotkeys_file:
            line = line.strip()
            if len(line) == 0 or line[0] == "[":
                output += line + "\n"
                continue
            pair = line.split("=")
            key = pair[0]
            values = pair[1].split(",")
            output += key + "="

            output += parse_pair(I18N_parser, key, values, layout_name, GLOBAL, altgr)
            output += "\n"

        hotkeys_file.close()
        filepath = layout_name + "/" + filename
        if not os.path.isdir(layout_name):
            os.makedirs(layout_name)
        fileio = open(filepath, 'w')
        fileio.write(output)
        fileio.close()
        if VERIFY_ALL:
            verify_file(filepath)

# Main part of the script. For each race, generate each layout, and translate that layout for large and small hands.

def remove_spaces(filepath):
    lines = []
    with open(filepath) as infile:
        for line in infile:
            line = line.replace(" ", "")
            lines.append(line)
    with open(filepath, 'w') as outfile:
        for line in lines:
            outfile.write(line)

def order(filepath):
    read_parser = SafeConfigParser()
    read_parser.optionxform = str
    read_parser.read(filepath)

    dict = {}
    for section in read_parser.sections():
        items = read_parser.items(section)
        items.sort()
        dict[section] = items

    open(filepath, 'w').close()  # clear file

    write_parser = SafeConfigParser()  # on other parser just for the safty
    write_parser.optionxform = str
    write_parser.read(filepath)

    write_parser.add_section("Settings")
    write_parser.add_section("Hotkeys")
    write_parser.add_section("Commands")

    for section in dict.keys():
        if not write_parser.has_section(section):
            write_parser.add_section(section)
        items = dict.get(section)
        for item in items:
            write_parser.set(section, item[0], item[1])

    file = open(filepath, 'w')
    write_parser.write(file)
    file.close()
    remove_spaces(filepath)


# NEW - Generate the file from TheCoreSeed.ini
def generate_seed_files(model):
    theseed_parser = SafeConfigParser()
    theseed_parser.optionxform = str
    theseed_parser.read('TheCoreSeed.ini')

    for race in races:
        filename = prefix + " " + race + "LM " + suffix
        filepath = Seed_files_folder + "/" + filename
        open(filepath, 'w').close()
        hotkeyfile_parser = SafeConfigParser()
        hotkeyfile_parser.optionxform = str

        for key in model.keys():
            hotkey = model[key]
            section = hotkey.section
            value = None
            while True:
                if hotkey.copyOf:
                    hotkey = model[hotkey.copyOf]
                else:
                    value = hotkey.get_value(race)
                    if value is None:
                        value = hotkey.default
                    break
            if not hotkeyfile_parser.has_section(section):
                hotkeyfile_parser.add_section(section)
            hotkeyfile_parser.set(section, key, value)
        hotkeyfile = open(filepath, 'w')
        hotkeyfile_parser.write(hotkeyfile)
        hotkeyfile.close()
        order(filepath)

def verify_seed_with_generate():
    print("-------------------------")
    print(" Start Comparing Seeds Files with Generated Files")

    for race in races:
        filepath_seed = prefix + " " + race + "LM " + suffix
        filepath_gen = Seed_files_folder + "/" + filepath_seed

        parser_seed = SafeConfigParser()
        parser_seed.optionxform = str
        parser_seed.read(filepath_seed)

        parser_gen = SafeConfigParser()
        parser_gen.optionxform = str
        parser_gen.read(filepath_gen)

        theseed_parser = SafeConfigParser()
        theseed_parser.optionxform = str
        theseed_parser.read('TheCoreSeed.ini')

        new_defaults_parser = SafeConfigParser()
        new_defaults_parser.optionxform = str
        new_defaults_parser.read('NewDefaults.ini')

        print("Race: " + race)
        print()

        print("In Seed not in Gen")
        for section in parser_seed.sections():
            for seed_item in parser_seed.items(section):
                key = seed_item[0]
                if not parser_gen.has_option(section, key):
                    print(key)
        print()
        print("In Seed diffrent in Gen")
        for section in new_defaults_parser.sections():
            for item in new_defaults_parser.items(section):
                key = item[0]
                if parser_gen.has_option(section, key) and parser_seed.has_option(section, key):
                    value_gen = parser_gen.get(section, key)
                    value_seed = parser_seed.get(section, key)
                    if value_seed != value_gen:
                        if theseed_parser.has_option(section, key):
                            original = theseed_parser.get(section, key)
                            print(key + " seed: " + value_seed + " gen: " + value_gen + " hint: copy of " + original)
                        else:
                            print(key + " seed: " + value_seed + " gen: " + value_gen)

        print()
        print("In Gen not in Seed (defaults filtered)")
        for section in parser_gen.sections():
            for gen_item in parser_gen.items(section):
                key = gen_item[0]
                value_gen = gen_item[1]
                if not parser_seed.has_option(section, key):
                    default = new_defaults_parser.get(section, key)
                    if value_gen != default:
                        if theseed_parser.has_option(section, key):
                            original = theseed_parser.get(section, key)
                            print(key + " gen: " + value_gen + " seed default: " + default + " hint: copy of " + original)
                        else:
                            print(key + " gen: " + value_gen + " seed default: " + default)
        print()
    print("-------------------------")

def generate_other_files():
    for race in races:
        filename = prefix + " " + race + "LM " + suffix
        filepath = Seed_files_folder + "/" + filename
        verify_file(filepath)
        translate_file(filename, False)
        translate_file(shift_hand_size(filename, True, "L", False), False)
        translate_file(shift_hand_size(filename, False, "S", False), False)
        for layout in layouts:
            index = layoutIndices[layout]
            layout_filename = generate_layout(filename, race, layout, index)
            translate_file(layout_filename, righty_index[index])
            if righty_index[index]:
                translate_file(shift_hand_size(layout_filename, True, "S", True), True)
                translate_file(shift_hand_size(layout_filename, False, "L", True), True)
            else:
                translate_file(shift_hand_size(layout_filename, True, "L", False), False)
                translate_file(shift_hand_size(layout_filename, False, "S", False), False)


def create_model():
    theseed_parser = SafeConfigParser()
    theseed_parser.optionxform = str
    theseed_parser.read('TheCoreSeed.ini')

    default_parser = SafeConfigParser()
    default_parser.optionxform = str
    default_parser.read('NewDefaults.ini')

    parsers = {}
    for race in races:
        filepath = prefix + " " + race + "LM " + suffix
        seed_hotkeyfile_parser = SafeConfigParser()
        seed_hotkeyfile_parser.optionxform = str
        seed_hotkeyfile_parser.read(filepath)
        parsers[race] = seed_hotkeyfile_parser

    model = {}
    for section in default_parser.sections():
        for item in default_parser.items(section):
            key = item[0]
            hotkey = Hotkey(key, section)

            default = item[1]
            hotkey.default = default

            for race in races:
                if parsers[race].has_option(section, key):
                    value = parsers[race].get(section, key)  #
                    hotkey.set_value(race, value)

            if theseed_parser.has_option(section, key):
                copyof = theseed_parser.get(section, key)
                hotkey.copyOf = copyof
            model[key] = hotkey

    return model

def new_keys_from_seed_hotkeys():
    default_filepath = 'NewDefaults.ini'
    default_parser = SafeConfigParser()
    default_parser.optionxform = str
    default_parser.read(default_filepath)

    for race in races:
        filepath = prefix + " " + race + "LM " + suffix
        seed_hotkeyfile_parser = SafeConfigParser()
        seed_hotkeyfile_parser.optionxform = str
        seed_hotkeyfile_parser.read(filepath)

        for section in seed_hotkeyfile_parser.sections():
            for item in seed_hotkeyfile_parser.items(section):
                key = item[0]
                if not default_parser.has_option(section, key):
                    default_parser.set(section, key, "")

    file = open(default_filepath, 'w')
    default_parser.write(file)
    file.close()
    order(default_filepath)

def check_defaults():
    default_filepath = 'NewDefaults.ini'
    default_parser = SafeConfigParser()
    default_parser.optionxform = str
    default_parser.read(default_filepath)
    
    ddefault_filepath = 'different_default.ini'
    ddefault_parser = SafeConfigParser()
    ddefault_parser.optionxform = str
    ddefault_parser.read(ddefault_filepath)
    
    theseed_parser = SafeConfigParser()
    theseed_parser.optionxform = str
    theseed_parser.read('TheCoreSeed.ini')
    
    parsers = {}
    for race in races:
        filepath = prefix + " " + race + "LM " + suffix
        seed_hotkeyfile_parser = SafeConfigParser()
        seed_hotkeyfile_parser.optionxform = str
        seed_hotkeyfile_parser.read(filepath)
        parsers[race] = seed_hotkeyfile_parser

    for section in default_parser.sections():
        for item in default_parser.items(section):
            key = item[0]
            default = item[1]
            multidefault = ddefault_parser.has_option(section, key)
            if not default or multidefault:
                seedhas = True
                for race in races:
                    if not parsers[race].has_option(section, key):
                        seedhas = False
                inherit = theseed_parser.has_option(section, key)
                
                if multidefault:
                    if not seedhas and not inherit:
                        print("[ERROR] multidefault not set in all seed layouts " + key)
                
                if not default:
                    if seedhas or inherit:
                        print("[WARN] no default " + key)
                    else:
                        print("[ERROR] no default " + key)

def suggest_inherit():
    print("------------------------------")
    print("suggest inherit")
    default_filepath = 'NewDefaults.ini'
    default_parser = SafeConfigParser()
    default_parser.optionxform = str
    default_parser.read(default_filepath)
    
    theseed_parser = SafeConfigParser()
    theseed_parser.optionxform = str
    theseed_parser.read('TheCoreSeed.ini')
    
    parsers = {}
    for race in races:
        hotkeyfile_parser = SafeConfigParser()
        hotkeyfile_parser.optionxform = str
        hotkeyfile_parser.read(prefix + " " + race + "LM " + suffix)
        parsers[race] = hotkeyfile_parser

    dict = {}
    for section in default_parser.sections():
        for item in default_parser.items(section):
            key = item[0]
            default = item[1]
            values = {}
            for race in races:
                if parsers[race].has_option(section, key):
                    value = parsers[race].get(section, key)
                else:
                    value = default
                values[race.index(race)] = value
            dict[key] = values
            
    outputdict = {}
    for key, values in dict.items():
        for key2, values2 in dict.items():
            if key == key2:
                continue
            
            equal = True
            for race in races:
                index = races.index(race)
                value = values.get(index)
                value2 = values2.get(index)
                if value != value2:
                    equal = False
                    break
                    
            if equal:
                key = ""
                for race in races:
                    index = races.index(race)
                    value = values.get(index)
                    key = key + race + ":" + str(value) + " "
                
                if not key in outputdict:
                    outputdict[key] = []
                if not item[0] in outputdict[key]:
                    outputdict[key].append(item[0])
                
    for values, listkeys in outputdict.items():
        print(values)
        listkeys.sort()
        for key in listkeys:
            copyofstr = ""
            for section in theseed_parser.sections():
                if theseed_parser.has_option(section, key):
                    seedini_value = theseed_parser.get(section, key)
                    copyofstr = " copy of " + seedini_value
                    break
            print("\t" + key + " " + copyofstr)
    print()

def wrong_inherit():
    print("------------------------------")
    print("Wrong inherit")
    default_filepath = 'NewDefaults.ini'
    default_parser = SafeConfigParser()
    default_parser.optionxform = str
    default_parser.read(default_filepath)
    
    theseed_parser = SafeConfigParser()
    theseed_parser.optionxform = str
    theseed_parser.read('TheCoreSeed.ini')
    parsers = {}
    for race in races:
        hotkeyfile_parser = SafeConfigParser()
        hotkeyfile_parser.optionxform = str
        hotkeyfile_parser.read(prefix + " " + race + "LM " + suffix)
        parsers[race] = hotkeyfile_parser

    dict = {}
    for section in default_parser.sections():
        for item in default_parser.items(section):
            key = item[0]
            values = {}
            for race in races:
                index = races.index(race)
                if parsers[race].has_option(section, key):
                    value = parsers[race].get(section, key)
                    values[index] = value
                else:
                    values[index] = ""
            dict[key] = values
    
    for section in theseed_parser.sections():
        for item in theseed_parser.items(section):
            key = item[0]
            copyofkey = item[1]
            values = dict[key]
            copyofvalues = dict[copyofkey]

            equal = True
            for race in races:
                index = races.index(race)
                value = values[index]
                copyofvalue = copyofvalues[index]
                if value != copyofvalue:
                    equal = False
            if not equal:
                print(key + " != " + copyofkey)
            
                print("\t" , end="")
                for race in races:
                    print(race + ": " + str(values[races.index(race)]), end=" ")
                print("= " + key)
            
                print("\t" , end="")
                for race in races:
                    print(race + ": " + str(copyofvalues[races.index(race)]), end=" ")
                print("= " + copyofkey)
        
    print()


#suggest_inherit()
#wrong_inherit()     
# check sections
new_keys_from_seed_hotkeys()
#check_defaults()
model = create_model()
generate_seed_files(model)
#verify_seed_with_generate()
if not ONLY_SEED:
    generate_other_files()

# Quick test to see if 4 seed files are error free
#     Todo:    expand this to every single file in every directory
#             expand both SAME_CHECKS and CONFLICT_CHECKS
# for race in races:
#    filename = prefix + " " + race + "LM " + suffix
#    verify_file(filename)

