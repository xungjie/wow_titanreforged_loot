local ALName, ALPrivate = ...
local AL = {}
_G.AtlasLootMY.Locales = AL

--lua
local _G = _G
local rawset = _G.rawset

-- save
local localeSave = {}

function _G.AtlasLootMY.GetLocales(locale)
	return ALPrivate.ACCOUNT_LOCALE == locale and AL or nil
end
AtlasLootMY.__al=localeSave
setmetatable(AL, {
	__index = function(self, key)
		--self[key] = key or ""
		return localeSave[key] or key--error(format("%s LOCALE NOT FOUND", key or "nil"))
	end,
	__newindex = function(self, key, value)
		rawset(localeSave, key, value == true and key or value)
	end,
	}
)
