export default function PlayerScoutingMidlane(props){
    const {value, panelIndex} = props

    return (
        <div className="wrapper-player-scouting-Midlane">
            <div
                role='tabpanbel'
                hidden={value !== panelIndex}
                className={`simple-tabpanel-${panelIndex}`}
                aria-labelledby={`simple-tab-${panelIndex}`}
            >
                <>
                    {
                        panelIndex === 2 &&
                        <p>Midlane</p>
                    }
                </>
            </div>
        </div>
    )
}