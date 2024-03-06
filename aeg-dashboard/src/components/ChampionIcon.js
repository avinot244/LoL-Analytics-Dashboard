import "../styles/ChampionIcon.css"

function ChampionIcon({championName, winRate, pickRate, banRate, pickOrder}){
    return (
        championName !== "" ?
        (<div className="champion-info">
            <img className="champion-icon-img" src={require(`../assets/champions/${championName}_0.jpg`)}/>
            <div className="champion-data">
                <p>{winRate}%</p>
                <p>{pickRate}%</p>
                <p>{banRate}%</p>
                <p>{pickOrder}</p>
            </div>
        </div>)
        :
        (<div className="champion-info">
            <div className="champion-icon"></div>
            <div className="champion-data">
                <p>{winRate}%</p>
                <p>{pickRate}%</p>
                <p>{banRate}%</p>
                <p>{pickOrder}</p>
            </div>
        </div>)
    )
}


export default ChampionIcon