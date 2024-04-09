import { useEffect, useState } from "react";
import "../styles/ChampionIcon.css"

function ChampionIcon({championName, winRate, pickRate, banRate, pickOrder}){
    const apiURL = `https://ddragon.leagueoflegends.com/cdn/14.5.1/img/champion/${championName}.png`
    const [img, setImg] = useState()

    const fetchImage = async () => {
        const res = await fetch(apiURL)
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
            <img className="champion-icon-img" src={img}/>
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