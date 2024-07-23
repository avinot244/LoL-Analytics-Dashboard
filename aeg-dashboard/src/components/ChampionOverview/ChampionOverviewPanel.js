import ChampionOverviewPanelBans from "./ChampionOverviewPanelBans";
import ChampionOverviewPanelPicks from "./ChampionOverviewPanelPicks";

export default function ChampionOverviewPanel(props) {
    const {value, panelIndex, tournament, patch, side} = props
    return (
        <>
            <ChampionOverviewPanelBans value={value} panelIndex={panelIndex} tournament={tournament} patch={patch} side={side}/>
            <ChampionOverviewPanelPicks value={value} panelIndex={panelIndex} tournament={tournament} patch={patch} side={side}/>
        </>
    )
}