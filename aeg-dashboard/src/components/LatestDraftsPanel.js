import DraftComponent from "./DraftComponent";

function LatestDraftsPanel(props) {
    const {value, panelIndex} = props
    return (
        <div
            role='tabpanbel'
            hidden={value !== panelIndex}
            className={`simple-tabpanel-${panelIndex}`}
            aria-labelledby={`simple-tab-${panelIndex}`}
        >

            <DraftComponent
                team1Name={"T1"}
                team2Name={"JDG"}
                picksB1rota={["Orianna", "Rell", "Aatrox"]}
                picksB2rota={["Jhin", "Bard"]}
                picksR1rota={["Rumble", "Akali", "Vi"]}
                picksR2rota={["Xayah", "Alistar"]}
                bansB1rota={["Rakan", "Neeko", "JarvanIV"]}
                bansB2rota={["Nautilus", "Renata"]}
                bansR1rota={["Ashe", "Poppy", "Kalista"]}
                bansR2rota={["Senna", "Caitlyn"]}
                win={0}
            />

            <DraftComponent
                team1Name={"JDG"}
                team2Name={"T1"}
                picksB1rota={["Orianna", "Belveth", "Aatrox"]}
                picksB2rota={["Zeri", "Lulu"]}
                picksR1rota={["JarvanIV", "Varus", "Azir"]}
                picksR2rota={["Yone", "Bard"]}
                bansB1rota={["Rumble", "Poppy", "Rell"]}
                bansB2rota={["Ashe", "Renata"]}
                bansR1rota={["Xayah", "Kaisa", "Kalista"]}
                bansR2rota={["Neeko", "Rakan"]}
                win={1}
            />

            <DraftComponent
                team1Name={"JDG"}
                team2Name={"T1"}
                picksB1rota={["Orianna", "Kalista", "Vi"]}
                picksB2rota={["KSante", "Senna"]}
                picksR1rota={["Caitlyn", "Ashe", "Azir"]}
                picksR2rota={["Maokai", "Aatrox"]}
                bansB1rota={["Rumble", "Poppy", "Akali"]}
                bansB2rota={["Gwen", "Rell"]}
                bansR1rota={["Rakan", "Neeko", "JarvanIV"]}
                bansR2rota={["Nautilus", "Blitzcrank"]}
                win={0}
            />

            <DraftComponent
                team1Name={"T1"}
                team2Name={"JDG"}
                picksB1rota={["Kalista", "Rell", "Azir"]}
                picksB2rota={["Aatrox", "Renata"]}
                picksR1rota={["Varus", "Ashe", "MonkeyKing"]}
                picksR2rota={["Taliyah", "Renekton"]}
                bansB1rota={["Rakan", "Neeko", "JarvanIV"]}
                bansB2rota={["Akali", "KSante"]}
                bansR1rota={["Rumble", "Orianna", "Poppy"]}
                bansR2rota={["Pyke", "Bard"]}
                win={0}
            />

            <DraftComponent
                team1Name={"M8"}
                team2Name={"KC"}
                picksB1rota={["Smolder", "Trundle", "Orianna"]}
                picksB2rota={["Aatrox", "Alistar"]}
                picksR1rota={["Volibear", "Nautilus", "Kaisa"]}
                picksR2rota={["Karma", "Jax"]}
                bansB1rota={["Senna", "Ivern", "Kalista"]}
                bansB2rota={["Jayce", "Tristana"]}
                bansR1rota={["Rell", "Maokai", "Varus"]}
                bansR2rota={["Gnar", "Braum"]}
                win={1}
            />
        
            <br/>
        </div>
        
    )
}

export default LatestDraftsPanel;