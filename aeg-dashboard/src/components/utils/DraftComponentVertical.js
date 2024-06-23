import ChampionIconSmallGlow from "./ChampionIconSmallGlow";
import "../../styles/DraftComponentVertical.css"

export default function DraftComponentVertical({team1Name, team2Name, picksB1rota, picksB2rota, bansB1rota, bansB2rota, picksR1rota, picksR2rota, bansR1rota, bansR2rota, win, championNameFilter}) {
    return (
        <>
            <div className="draft-content-vertical">
                <div className="blue-vertical">
                    <div className="header-team-vertical">
                        {
                            win === 0 ? (
                                <h1 className="win">WIN</h1>
                            ) : (
                                <h1 className="lose">LOSE</h1>
                            )
                        }
                        <h1 className="teamName">{team1Name}</h1>
                    </div>
                    <div className="blue-pb-vertical">
                        <div className="bansBlue-vertical">
                            <div className="bansBlue1Rota-vertical">
                                <ul className="vertical">
                                    {bansB1rota.map((championName) => 
                                        {
                                            if (championName !== championNameFilter) {
                                                return (
                                                    <li>
                                                        <ChampionIconSmallGlow
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
                                                        <ChampionIconSmallGlow
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
                            <div className="bansBlue2Rota-vertical">
                                <ul className="vertical">
                                    {bansB2rota.map((championName) =>
                                        {
                                            if (championName !== championNameFilter) {
                                                return (
                                                    <li>
                                                        <ChampionIconSmallGlow
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
                                                        <ChampionIconSmallGlow
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
                        <div className="picksBlue-vertical">
                            <div className="picksBlue1Rota-vertical">
                                <ul className="vertical">
                                    {picksB1rota.map((championName) => {
                                        if (championName !== championNameFilter) {
                                            return (
                                                <li>
                                                    <ChampionIconSmallGlow
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
                                                    <ChampionIconSmallGlow
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
                            <div className="picksBlue2Rota-vertical">
                                <ul className="vertical">
                                    {picksB2rota.map((championName) =>
                                        {
                                            if (championName !== championNameFilter) {
                                                return (
                                                    <li>
                                                        <ChampionIconSmallGlow
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
                                                        <ChampionIconSmallGlow
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
                    </div>
                    
                </div>

                <div className="red-vertical">
                    <div className="header-team-vertical">
                        <h1 className="teamName">{team2Name}</h1>

                        {
                            win === 1 ? (
                                <h1 className="win">WIN</h1>
                            ) : (
                                <h1 className="lose">LOSE</h1>
                            )
                        }
                    </div>
                    <div className="red-pb-vertical">
                        <div className="picksRed-vertical">
                            <div className="picksRed1Rota-vertical">
                                <ul className="vertical">
                                    {picksR1rota.map((championName) =>
                                        {
                                            if (championName !== championNameFilter) {
                                                return (
                                                    <li>
                                                        <ChampionIconSmallGlow
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
                                                        <ChampionIconSmallGlow
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
                            <div className="picksRed2Rota-vertical">
                                <ul className="vertical">
                                    {picksR2rota.map((championName) =>
                                        {
                                            if (championName !== championNameFilter) {
                                                return (
                                                    <li>
                                                        <ChampionIconSmallGlow
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
                                                        <ChampionIconSmallGlow
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
                        <div className="bansRed-vertical">
                            <div className="bansRed1Rota-vertical">
                                <ul className="vertical">
                                    {bansR1rota.map((championName) => 
                                        {
                                            if (championName !== championNameFilter) {
                                                return (
                                                    <li>
                                                        <ChampionIconSmallGlow
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
                                                        <ChampionIconSmallGlow
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
                            <div className="bansRed2Rota-vertical">
                                <ul className="vertical">
                                    {bansR2rota.map((championName) =>
                                        {
                                            if (championName !== championNameFilter) {
                                                return (
                                                    <li>
                                                        <ChampionIconSmallGlow
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
                                                        <ChampionIconSmallGlow
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
            </div>
        </>
    )
}