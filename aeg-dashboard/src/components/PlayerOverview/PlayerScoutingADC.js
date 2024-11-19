export default function PlayerScoutingADC(props){
    const {value, panelIndex} = props

    return (
        <div className="wrapper-player-scouting-ADC">
            <div
                role='tabpanbel'
                hidden={value !== panelIndex}
                className={`simple-tabpanel-${panelIndex}`}
                aria-labelledby={`simple-tab-${panelIndex}`}
            >
                <>
                    {
                        panelIndex === 3 &&
                        <p>ADC</p>
                    }
                </>
            </div>
        </div>
    )
}