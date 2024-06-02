import "../styles/DraftComponent.css"
import ChampionIconSmall from "./ChampionIconSmall";


function DraftComponent({team1Name, team2Name, picksB1rota, picksB2rota, bansB1rota, bansB2rota, picksR1rota, picksR2rota, bansR1rota, bansR2rota, win, championNameFilter}) {
    // 0 : win Rlue, 1 : win Red

    return (
        <>
            <div className="draft-content">
                <div className="blue">
                    <div className="header-team">
                        {
                            win === 0 ? (
                                <h1 className="win">WIN</h1>
                            ) : (
                                <h1 className="lose">LOSE</h1>
                            )
                        }
                        <h1 className="teamName">{team1Name}</h1>
                    </div>
                    <div className="picksBlue">
                        <div className="picksBlue1Rota">
                            <ul className="horizontal">
                                {picksB1rota.map((championName) => {
                                    if (championName !== championNameFilter) {
                                        return (
                                            <li>
                                                <ChampionIconSmall
                                                    championName={championName}
                                                    width={80}
                                                    height={80}
                                                    glow={true}
                                                />
                                            </li>
                                        )
                                    } else {
                                        return (
                                            <li>
                                                <ChampionIconSmall
                                                    championName={championName}
                                                    width={80}
                                                    height={80}
                                                />
                                            </li>
                                        )
                                    }
                                }
                                    
                                )}
                            </ul>
                        </div>
                        <div className="picksBlue2Rota">
                            <ul className="horizontal">
                                {picksB2rota.map((championName) =>
                                    {
                                        if (championName != championNameFilter) {
                                            return (
                                                <li>
                                                    <ChampionIconSmall
                                                        championName={championName}
                                                        width={80}
                                                        height={80}
                                                        glow={true}
                                                    />
                                                </li>
                                            )
                                        } else {
                                            return (
                                                <li>
                                                    <ChampionIconSmall
                                                        championName={championName}
                                                        width={80}
                                                        height={80}
                                                    />
                                                </li>
                                            )
                                        }
                                    }
                                )}
                            </ul>
                        </div>
                    </div>
                    

                    <div className="bansBlue">
                        <div className="bansBlue1Rota">
                            <ul className="horizontal">
                                {bansB1rota.map((championName) => 
                                    {
                                        if (championName != championNameFilter) {
                                            return (
                                                <li>
                                                    <ChampionIconSmall
                                                        championName={championName}
                                                        width={50}
                                                        height={50}
                                                        glow={true}
                                                    />
                                                </li>
                                            )
                                        } else {
                                            return (
                                                <li>
                                                    <ChampionIconSmall
                                                        championName={championName}
                                                        width={50}
                                                        height={50}
                                                    />
                                                </li>
                                            )
                                        }
                                    }
                                )}
                                
                            </ul>
                        </div>
                        <div className="bansBlue2Rota">
                            <ul className="horizontal">
                                {bansB2rota.map((championName) =>
                                    {
                                        if (championName != championNameFilter) {
                                            return (
                                                <li>
                                                    <ChampionIconSmall
                                                        championName={championName}
                                                        width={50}
                                                        height={50}
                                                        glow={true}
                                                    />
                                                </li>
                                            )
                                        } else {
                                            return (
                                                <li>
                                                    <ChampionIconSmall
                                                        championName={championName}
                                                        width={50}
                                                        height={50}
                                                    />
                                                </li>
                                            )
                                        }
                                    }
                                )}
                            </ul>
                        </div>
                    </div>
                </div>

                <div className="red">
                    <div className="header-team">
                        <h1 className="teamName">{team2Name}</h1>
                        {
                            win === 1 ? (
                                <h1 className="win">WIN</h1>
                            ) : (
                                <h1 className="lose">LOSE</h1>
                            )
                        }
                    </div>
                    <div className="picksRed">
                        <div className="picksRed1Rota">
                            <ul className="horizontal">
                                {picksR1rota.map((championName) =>
                                    {
                                        if (championName != championNameFilter) {
                                            return (
                                                <li>
                                                    <ChampionIconSmall
                                                        championName={championName}
                                                        width={80}
                                                        height={80}
                                                        glow={true}
                                                    />
                                                </li>
                                            )
                                        } else {
                                            return (
                                                <li>
                                                    <ChampionIconSmall
                                                        championName={championName}
                                                        width={80}
                                                        height={80}
                                                    />
                                                </li>
                                            )
                                        }
                                    }
                                )}    
                            </ul>
                        </div>
                        <div className="picksRed2Rota">
                            <ul className="horizontal">
                                {picksR2rota.map((championName) =>
                                    {
                                        if (championName != championNameFilter) {
                                            return (
                                                <li>
                                                    <ChampionIconSmall
                                                        championName={championName}
                                                        width={80}
                                                        height={80}
                                                        glow={true}
                                                    />
                                                </li>
                                            )
                                        } else {
                                            return (
                                                <li>
                                                    <ChampionIconSmall
                                                        championName={championName}
                                                        width={80}
                                                        height={80}
                                                    />
                                                </li>
                                            )
                                        }
                                    }
                                )}
                            </ul>
                        </div>
                    </div>
                    <div className="bansRed">
                        <div className="bansRed1Rota">
                            <ul className="horizontal">
                                {bansR1rota.map((championName) => 
                                    {
                                        if (championName != championNameFilter) {
                                            return (
                                                <li>
                                                    <ChampionIconSmall
                                                        championName={championName}
                                                        width={50}
                                                        height={50}
                                                        glow={true}
                                                    />
                                                </li>
                                            )
                                        } else {
                                            return (
                                                <li>
                                                    <ChampionIconSmall
                                                        championName={championName}
                                                        width={50}
                                                        height={50}
                                                    />
                                                </li>
                                            )
                                        }
                                    }
                                )}
                            </ul>
                        </div>
                        <div className="bansRed2Rota">
                            <ul className="horizontal">
                                {bansR2rota.map((championName) =>
                                    {
                                        if (championName != championNameFilter) {
                                            return (
                                                <li>
                                                    <ChampionIconSmall
                                                        championName={championName}
                                                        width={50}
                                                        height={50}
                                                        glow={true}
                                                    />
                                                </li>
                                            )
                                        } else {
                                            return (
                                                <li>
                                                    <ChampionIconSmall
                                                        championName={championName}
                                                        width={50}
                                                        height={50}
                                                    />
                                                </li>
                                            )
                                        }
                                    }
                                )}
                            </ul>
                        </div>
                    </div>
                </div>                
            </div>
        </>
    )
}

export default DraftComponent;