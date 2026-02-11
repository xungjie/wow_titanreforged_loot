local AtlasLoot = _G.AtlasLootMY
local GUI = AtlasLoot.GUI
local ChangelogFrame = {}
AtlasLoot.GUI.ChangelogFrame = ChangelogFrame
local AL = AtlasLoot.Locales


function ChangelogFrame.Create(parent)
    local changelogFrame = CreateFrame("Frame", "AtlasMY_ChangelogFrame", parent,"BasicFrameTemplateWithInset")
    changelogFrame:SetSize(500, 300)
    changelogFrame:SetPoint("CENTER", parent, "CENTER", 0, 0)
    changelogFrame:SetFrameStrata("DIALOG")
    changelogFrame:SetMovable(true)
    changelogFrame:EnableMouse(true)
    changelogFrame:RegisterForDrag("LeftButton")
    changelogFrame:SetScript("OnDragStart", changelogFrame.StartMoving)
    changelogFrame:SetScript("OnDragStop", changelogFrame.StopMovingOrSizing)
    --tinsert(UISpecialFrames, "AtlasMY_ChangelogFrame")
    -- 设置标题
    changelogFrame.title = changelogFrame:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    changelogFrame.title:SetPoint("TOP", 0, -5)
    changelogFrame.title:SetText("更新日志")

    -- 创建滚动框架
    changelogFrame.scrollFrame = CreateFrame("ScrollFrame", nil, changelogFrame, "UIPanelScrollFrameTemplate")
    changelogFrame.scrollFrame:SetPoint("TOPLEFT", 10, -30)
    changelogFrame.scrollFrame:SetPoint("BOTTOMRIGHT", -30, 10)
    
    -- 创建文本内容框架
    changelogFrame.content = CreateFrame("Frame", nil, changelogFrame.scrollFrame)
    changelogFrame.content:SetWidth(460)
    -- 创建更新日志文本
    changelogFrame.text = changelogFrame.content:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    changelogFrame.text:SetPoint("TOPLEFT", 10, -10)
    changelogFrame.text:SetJustifyH("LEFT")
    changelogFrame.text:SetJustifyV("TOP")
    changelogFrame.text:SetWidth(460)
    changelogFrame.text:SetWordWrap(true)
    changelogFrame.text:SetText(AL['changelogText'])
    local textHeight = changelogFrame.text:GetStringHeight()
    -- 设置子框架的高度为文本高度
    changelogFrame.content:SetHeight(textHeight)
    changelogFrame.scrollFrame:SetScrollChild(changelogFrame.content)
    
    return changelogFrame
end

