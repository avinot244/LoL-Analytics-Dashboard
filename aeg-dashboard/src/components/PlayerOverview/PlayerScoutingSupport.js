export default function PlayerScoutingSupport(props){
    const {value, panelIndex} = props

    return (
        <div className="wrapper-player-scouting-Support">
            <div
                role='tabpanbel'
                hidden={value !== panelIndex}
                className={`simple-tabpanel-${panelIndex}`}
                aria-labelledby={`simple-tab-${panelIndex}`}
            >
                <>
                    {
                        panelIndex === 4 &&
                        <p>Support</p>
                    }
                </>
            </div>
        </div>
    )
}