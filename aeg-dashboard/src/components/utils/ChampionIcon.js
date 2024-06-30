import { useEffect, useState, useContext } from "react";
import "../../styles/ChampionIcon.css"
import AuthContext from "../context/AuthContext";

function ChampionIcon({championName, winRate, pickRate, banRate, pickOrder}){
    const [img, setImg] = useState()
    let {patch} = useContext(AuthContext)
    const fetchImage = async () => {
        const res = await fetch(`https://ddragon.leagueoflegends.com/cdn/${patch}/img/champion/${championName}.png`)
        const imageBlob = await res.blob()
        const imageObjectURL = URL.createObjectURL(imageBlob);
        setImg(imageObjectURL);
    };

    useEffect(() => {
        fetchImage();
    }, [])

    return (
        championName !== "" ?
        (<div className="champion-info">
            <img className="champion-icon-img" src={img} alt={championName}/>
            <div className="champion-data">
                <p>WR : <span>{winRate}%</span></p>
                <p>Pick : <span>{pickRate}%</span></p>
                <p>Ban : <span>{banRate}%</span></p>
                <p>Pickorder : <span>{pickOrder}</span></p>
            </div>
        </div>)
        :
        (<div className="champion-info">
            <div className="champion-icon"></div>
            <div className="champion-data">
                <p>WR : <span>{winRate}%</span></p>
                <p>Pick : <span>{pickRate}%</span></p>
                <p>Ban : <span>{banRate}%</span></p>
                <p>Pickorder : <span>{pickOrder}</span></p>
            </div>
        </div>)
    )
}


export default ChampionIcon