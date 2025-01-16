import { SliderMarkLabel, Tooltip } from "@mui/material";
import dragonIcon from "../../../assets/objectives/dragon.png"
import towerIcon from "../../../assets/objectives/tower.png"
import grubIcon from "../../../assets/objectives/grub.png"
import riftheraldIcon from "../../../assets/objectives/riftherald.png"
import inhibitorIcon from "../../../assets/objectives/inhibitor.png"
import nexusIcon from "../../../assets/objectives/nexus.png"
import baronIcon from "../../../assets/objectives/baron.png"


export const CustomMark = (props) => {
    console.log(props)
    const index = props["data-index"];
    const mark = props.ownerState.marks[index]

    const isTop = index % 2 !== 0;

    const baseStyles = {
        height: "fit-content",
        width: "fit-content",
        color: "white",
    };
    const topRowStyles = {
        ...baseStyles,
        ...{
            top: "-24px",
        },
    };
    
    const customMarkStyles = isTop ? topRowStyles : baseStyles;

    return (
        <Tooltip title={mark.label} placement={isTop ? "top" : "bottom"} arrow>
            <SliderMarkLabel
                {...props}
                style={{
                    ...props.style,
                    ...customMarkStyles,
                }}
            >
                <div
                    style={{
                        marginLeft: 8,
                        marginRight: 8,
                    }}
                >
                    {
                        mark.label === "turret" ?  (
                            <img src={towerIcon} width={25}/>
                        ) : mark.label === "dragon" ? (
                            <img src={dragonIcon} width={25}/>
                        ) : mark.label === "VoidGrub" ? (
                            <img src={grubIcon} width={25}/>
                        ) : mark.label === "riftHerald" ? (
                            <img src={riftheraldIcon} width={25}/>
                        ) : mark.label === "inhibitor" ? (
                            <img src={inhibitorIcon} width={25}/>
                        ) : mark.label === "nexus" ? (
                            <img src={nexusIcon} width={25}/>
                        ) : mark.label === "baron" ? (
                            <img src={baronIcon} width={25}/>
                        ) : (
                            <></>
                        )
                    }
                </div>
            </SliderMarkLabel>
        </Tooltip>
    );
};