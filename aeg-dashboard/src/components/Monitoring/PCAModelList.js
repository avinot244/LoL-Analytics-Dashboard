import { Button } from "@mui/material";
import React from "react";
import {Table} from "react-bootstrap"
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import DeleteIcon from '@mui/icons-material/Delete';

export default function PCAModelList ({modelList}) {
    return (
        <Table dark>
            <thead>
                <th>UUID</th>
                <th>role</th>
                <th>KMO</th>
            </thead>
            <tbody>
                {!modelList || modelList.length <= 0 ? (
                    <tr>
                        <td colSpan={6} align="center">
                            <b>Oops, no data yet</b>
                        </td>
                    </tr>
                ) : (
                    modelList.map(model => (
                        <tr key={model.pk}>
                            <td>{model.uuid}</td>
                            <td>{model.role}</td>
                            <td>{model.kmo}</td>
                            <td align="center">
                                <Button
                                    endIcon={<ArrowForwardIosIcon/>}
                                    variant="contained"
                                >
                                    Analyze
                                </Button>

                                <Button
                                    endIcon={<ArrowDownwardIcon/>}
                                    sx={{
                                        ml: 2
                                    }}
                                    variant="contained"
                                >
                                    Set
                                </Button>

                                <Button
                                    endIcon={<DeleteIcon/>}
                                    sx={{
                                        ml: 2
                                    }}
                                    variant="contained"
                                    color="error"
                                >
                                    Delete
                                </Button>
                            </td>
                        </tr>
                    ))
                )

                }
            </tbody>
        </Table>
    )

}