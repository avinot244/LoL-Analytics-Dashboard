import { Switch } from "@mui/material";
import { yellow } from '@mui/material/colors';
import { alpha, styled } from '@mui/material/styles';

const YellowSwitch = styled(Switch)(({ theme }) => ({
    '& .MuiSwitch-switchBase.Mui-checked': {
        color: yellow[600],
        '&:hover': {
            backgroundColor: alpha(yellow[600], theme.palette.action.hoverOpacity),
        },
    },
    '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
        backgroundColor: yellow[600],
    },
}));

export default YellowSwitch