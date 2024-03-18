function LatestDraftsPanel(props) {
    const {value, panelIndex} = props
    return (
        <div
            role='tabpanbel'
            hidden={value !== panelIndex}
            className={`simple-tabpanel-${panelIndex}`}
            aria-labelledby={`simple-tab-${panelIndex}`}
        >
            LatestDrafts
        </div>
    )
}

export default LatestDraftsPanel;