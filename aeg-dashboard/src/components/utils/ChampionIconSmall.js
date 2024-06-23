import { useState, useEffect } from "react";
import "../../styles/ChampionIconSmall.css"

function ChampionIconSmall({championName, width, height}) {
    const apiURL = `https://ddragon.leagueoflegends.com/cdn/14.5.1/img/champion/${championName}.png`
    const [img, setImg] = useState();

    const fetchImage = async () => {
        const res = await fetch(apiURL);
        const imageBlob = await res.blob();
        const imageObjectURL = URL.createObjectURL(imageBlob);
        setImg(imageObjectURL);
    };

    useEffect(() => {
        fetchImage();
    }, []);



    return (
        <img className="champion-icon-small" src={img} alt={championName} width={width} height={height}/>
    )


    
}

export default ChampionIconSmall;