import "../styles/ChampionIcon.css"

function ChampionIcon({championName, winRate, pickRate}){
    return (
        <div className="champion-info">
            <img className="champion-icon-img" src={require(`../assets/champions/${championName}_0.jpg`)}/>
            <div className="champion-data">
                <p>{winRate}%</p>
                <p>{pickRate}%</p>
            </div>
        </div>
    )
}


export default ChampionIcon