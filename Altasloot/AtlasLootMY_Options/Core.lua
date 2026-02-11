local _G = getfenv(0)
local LibStub = _G.LibStub

local AtlasLoot = _G.AtlasLootMY
local Options = {}
local AL = AtlasLoot.Locales

AtlasLoot.Options = Options
local db = AtlasLoot.db
local globalDb = AtlasLoot.dbGlobal

local AceGUI = LibStub("AceGUI-3.0")
local AceConfig = LibStub("AceConfig-3.0")
local AceConfigDialog = LibStub("AceConfigDialog-3.0")
local AceDBOptions = LibStub("AceDBOptions-3.0")
local AceConfigRegistry = LibStub("AceConfigRegistry-3.0")
local catId
Options.orderNumber = 0

function Options:Show()
	Settings.OpenToCategory(catId)
	--AceConfigDialog:Open("AtlasLootMY")
end

function Options:Close()
	AceConfigDialog:Close("AtlasLootMY")
end

function Options:NotifyChange()
	AceConfigRegistry:NotifyChange("AtlasLootMY")
end

function Options:ShowAddon(addonName)
	AceConfigDialog:Open("AtlasLootMY", nil, "addons", addonName)
	--Settings.OpenToCategory(catId,"addons",addonName)
end

-- https://www.wowace.com/projects/ace3/pages/ace-gui-3-0-widgets
-- https://www.wowace.com/projects/ace3/pages/ace-config-3-0-options-tables
Options.config = {
	type = "group",
	name = AL["AtlasLoot - Titan"],
	args = {
	},
}

AceConfig:RegisterOptionsTable("AtlasLootMY", Options.config)
AceConfigDialog:SetDefaultSize("AtlasLootMY", 810, 550)
catId=select(2,AceConfigDialog:AddToBlizOptions("AtlasLootMY",AL["AtlasLoot - MiaoYing"]))

-- Add profile on last position
Options.config.args.profiles = AceDBOptions:GetOptionsTable(AtlasLoot.dbRaw)
Options.config.args.profiles.order = -30