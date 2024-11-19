export default function PlayerScoutingJungle(props){
    const {value, panelIndex} = props

    return (
        <div className="wrapper-player-scouting-Jungle">
            <div
                role='tabpanbel'
                hidden={value !== panelIndex}
                className={`simple-tabpanel-${panelIndex}`}
                aria-labelledby={`simple-tab-${panelIndex}`}
            >
                <>
                    {
                        panelIndex === 1 &&
                        <p>Jungle</p>
                    }
                </>
            </div>
        </div>
    )
}