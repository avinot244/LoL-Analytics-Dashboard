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