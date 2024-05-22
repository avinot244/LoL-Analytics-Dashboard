
import { Component, useState, useEffect } from "react";
import PropTypes from 'prop-types';
import { alpha } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import TableSortLabel from '@mui/material/TableSortLabel';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import Checkbox from '@mui/material/Checkbox';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';

import SearchIcon from '@mui/icons-material/Search';
import DeleteIcon from '@mui/icons-material/Delete';

import FilterListIcon from '@mui/icons-material/FilterList';
import { visuallyHidden } from '@mui/utils';

import "../../styles/PCAModelList.css"
import { API_URL } from "../../constants";
import { Button, Stack, selectClasses } from "@mui/material";


import ModalAnalyze from "./ModalAnalyze";

function descendingComparator(a, b, orderBy) {
    if (b[orderBy] < a[orderBy]) {
        return -1;
    }
    if (b[orderBy] > a[orderBy]) {
        return 1;
    }
    return 0;
}

function getComparator(order, orderBy) {
    return order === 'desc'
        ? (a, b) => descendingComparator(a, b, orderBy)
        : (a, b) => -descendingComparator(a, b, orderBy);
}

// Since 2020 all major browsers ensure sort stability with Array.prototype.sort().
// stableSort() brings sort stability to non-modern browsers (notably IE11). If you
// only support modern browsers you can replace stableSort(exampleArray, exampleComparator)
// with exampleArray.slice().sort(exampleComparator)
function stableSort(array, comparator) {
    const stabilizedThis = array.map((el, index) => [el, index]);
    stabilizedThis.sort((a, b) => {
        const order = comparator(a[0], b[0]);
        if (order !== 0) {
            return order;
        }
        return a[1] - b[1];
    });
    return stabilizedThis.map((el) => el[0]);
}

const headCells = [
    {
        id: 'uuid',
        numeric: false,
        disablePadding: true,
        label: 'Model UUID'
    },
    {
        id: 'role',
        numeric: false,
        disablePadding: true,
        label: 'Role'
    },
    {
        id: 'kmo',
        numeric: true,
        disablePadding: true,
        label: 'KMO'
    }
]

function EnhancedTableHead(props) {
    const { onSelectAllClick, order, orderBy, numSelected, rowCount, onRequestSort } = props;
    const createSortHandler = (property) => (event) => {
        onRequestSort(event, property);
    };

    return (
        <TableHead>
            <TableRow>
                <TableCell padding="checkbox">
                    <Checkbox
                        color="primary"
                        indeterminate={numSelected > 0 && numSelected < rowCount}
                        checked={rowCount > 0 && numSelected === rowCount}
                        onChange={onSelectAllClick}
                        inputProps={{
                            'aria-label': 'select all Champions',
                        }}
                    />
                </TableCell>

                {headCells.map((headCell) => (
                    <TableCell
                        key={headCell.id}
                        align={headCell.numeric ? 'right' : 'left'}
                        padding={headCell.disablePadding ? 'none' : 'normal'}
                        sortDirection={orderBy === headCell.id ? order : false}
                        sx={{pr: "15px"}}
                    >
                        <TableSortLabel
                            active={orderBy === headCell.id}
                            direction={orderBy === headCell.id ? order : 'asc'}
                            onClick={createSortHandler(headCell.id)}
                        >
                            {headCell.label}
                            {orderBy === headCell.id ? (
                                <Box component="span" sx={visuallyHidden}>
                                    {order === 'desc' ? 'sorted descending' : 'sorted ascending'}
                                </Box>
                            ) : null}
                        </TableSortLabel>
                    </TableCell>
                ))}
            </TableRow>
        </TableHead>
    );
}

EnhancedTableHead.propTypes = {
    numSelected: PropTypes.number.isRequired,
    onRequestSort: PropTypes.func.isRequired,
    onSelectAllClick: PropTypes.func.isRequired,
    order: PropTypes.oneOf(['asc', 'desc']).isRequired,
    orderBy: PropTypes.string.isRequired,
    rowCount: PropTypes.number.isRequired,
};


class EnhancedTableToolbar extends Component {
    state = {
        open: false,
        numSelected: this.props.numSelected,
        selectedModels: this.props.selectedModels
    };
    componentDidUpdate(prevProps) {
        if (prevProps.numSelected !== this.props.numSelected) {
            this.setState({
                numSelected: this.props.numSelected, 
                selectModels: this.props.selectedModels
            })
        }
    }

    handleOpen = () => {
        this.setState({
            open: true,
        })
    }

    handleClose = () => {
        this.setState({
            open: false
        })
    }

    handleDelete = async (selectedModels) => {
        selectedModels.map(async (model) => {
            const result = await fetch(API_URL + `behaviorModels/delete/${model.uuid}/${model.role}/`, {
                method: "DELETE"
            }).then(_ => {
                let temp = this.props.flag + 1
                this.props.setFlag(temp)
                this.props.setSelected([])
                this.setState({
                    numSelected: 0
                })
            })
        })
        
    }

    render () {
        return (
            <Toolbar
                sx={{
                    pl: { sm: 2 },
                    pr: { xs: 1, sm: 1 },
                    ...(this.state.numSelected > 0 && {
                    bgcolor: (theme) =>
                        alpha(theme.palette.primary.main, theme.palette.action.activatedOpacity),
                    }),
                }}
            >
            {this.state.numSelected > 0 ? (
                <Typography
                    sx={{ flex: '1 1 100%' }}
                    color="inherit"
                    variant="subtitle1"
                    component="div"
                >
                    
                </Typography>
                ) : (
                    <Typography
                        sx={{ flex: '1 1 100%' }}
                        variant="h6"
                        id="tableTitle"
                        component="div"
                    >
                        PCA Model List
                    </Typography>
            )}

            {this.state.numSelected > 0 && this.state.numSelected < 2 ? 
                (
                    <Tooltip>
                        <Stack spacing={2} direction="row" justifyContent="center" alignItems="center">
                            <Button
                                variant="contained"
                                endIcon={<SearchIcon/>}
                                onClick={() => {
                                    this.handleOpen()
                                }}
                            >
                                Analyze
                            </Button>
                            {this.state.open && 
                                <ModalAnalyze
                                    open={this.state.open}
                                    handleClose={this.handleClose}
                                    model={this.props.selectedModels[0]}
                                    flag={this.props.flag}
                                    setFlag={this.props.setFlag}
                                    setSelected={this.props.setSelected}
                                />
                            }
                            

                            <Button
                                variant="contained"
                                color="error"
                                endIcon={<DeleteIcon/>}
                                onClick={() => {
                                    this.handleDelete(this.props.selectedModels)
                                }}
                            >
                                Delete
                            </Button>
                        </Stack>
                        
                    </Tooltip>
                ) 
                : this.state.numSelected < 1 ? 
                (
                    <Tooltip>
                        <IconButton>
                            <FilterListIcon />
                        </IconButton>
                    </Tooltip>
                )
                : 
                (
                    <Tooltip>
                        <Button
                                variant="contained"
                                color="error"
                                endIcon={<DeleteIcon/>}
                                onClick={() => {
                                    this.handleDelete(this.state.selectedModels)
                                }}
                            >
                                Delete
                            </Button>
                    </Tooltip>
                )}
            </Toolbar>
        )
    }
}



export default function PCAModelList () {
    const [order, setOrder] = useState('asc');
    const [orderBy, setOrderBy] = useState('championName');
    const [selected, setSelected] = useState([]);
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(10);
    const [modelList, setModelList] = useState([])
    const [modelListFlag, setFlagModelList] = useState(1)


    const fetchPCAModels = async () => {
        const result = await fetch(API_URL + `behaviorModels/getAll/`, {
            method: "GET"
        })
        result.json().then(result => {
            let newModelList = []
            for (let i = 0; i < result.length ; i++) {
                let modelObject = result[i]
                let temp = {
                    "pk": modelObject.pk,
                    "uuid": modelObject.uuid,
                    "role": modelObject.role,
                    "kmo": (modelObject.kmo).toFixed(2),
                    "nbFactors": modelObject.nbFactors,
                    "selected": modelObject.selected,
                    "factorsName": modelObject.factorsName
                }
                newModelList.push(temp)
            }
            setModelList(newModelList)
        })
    }


    useEffect(() => {
        fetchPCAModels()
    }, [modelListFlag])

    const handleRequestSort = (event, property) => {
        const isAsc = orderBy === property && order === 'asc';
        setOrder(isAsc ? 'desc' : 'asc');
        setOrderBy(property);
    };

    const handleSelectAllClick = (event) => {
        if (event.target.checked) {
            const newSelected = modelList.map((n) => n);
            setSelected(newSelected);
            console.log(newSelected)
            return;
        }
        setSelected([]);
    };

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    const isSelected = (row) => {
        return selected.indexOf(row) !== -1;
    }

    // Avoid a layout jump when reaching the last page with empty rows.
    const emptyRows =
        page > 0 ? Math.max(0, (1 + page) * rowsPerPage - modelList.length) : 0;

    
    const visibleRows = stableSort(modelList, getComparator(order, orderBy)).slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
    // const visibleRows = React.useMemo(
    //     () => stableSort(modelList, getComparator(order, orderBy)).slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage),
    //     [order, orderBy, page, rowsPerPage],
    // );

    const handleClick = (event, row) => {
        const selectedIndex = selected.indexOf(row);
        let newSelected = [];

        if (selectedIndex === -1) {
            newSelected = newSelected.concat(selected, row)
        } else if (selectedIndex === 0) {
            newSelected = newSelected.concat(selected.slice(1));
        }
        else if (selectedIndex === selected.length - 1) {
            newSelected = newSelected.concat(selected.slice(0, -1));
        } else if (selectedIndex > 0) {
            newSelected = newSelected.concat(
                selected.slice(0, selectedIndex),
                selected.slice(selectedIndex + 1),
            );
        }
        setSelected(newSelected);
    };
    return (
        <div className='wrapper-tabpanel-pcaModelList'>
            <Box>
                <Paper sw={{width: '100%', mb: 2}}>
                    <EnhancedTableToolbar numSelected={selected.length} selectedModels={selected} setFlag={setFlagModelList} flag={modelListFlag} setSelected={setSelected}/>
                    <TableContainer>
                        <Table
                            sx={{ minWidth: 750, pr: 5}}
                            aria-labelledby="tableTitle"

                            size={'small'}
                        >
                            <EnhancedTableHead
                                numSelected={selected.length}
                                order={order}
                                orderBy={orderBy}
                                onSelectAllClick={handleSelectAllClick}
                                onRequestSort={handleRequestSort}
                                rowCount={modelList.length}
                            />
                            <TableBody>
                            {visibleRows.map((row, index) => {
                                const isItemSelected = isSelected(row);
                                const labelId = `enhanced-table-checkbox-${index}`;

                                if (row.selected) {
                                    return (
                                        <TableRow
                                            onClick={(event) => handleClick(event, row)}
                                            role="checkbox"
                                            aria-checked={isItemSelected}
                                            tabIndex={-1}
                                            key={row.id}
                                            selected={isItemSelected}
                                            sx={{ cursor: 'pointer'}}
                                        >
                                            <TableCell padding="checkbox">
                                                <Checkbox
                                                    color="primary"
                                                    checked={isItemSelected}
                                                    inputProps={{
                                                        'aria-labelledby': labelId,
                                                    }}
                                                />
                                            </TableCell>
                                            <TableCell sx={{fontWeight: 'bold', color: 'primary.main'}} align="left">{row.uuid}</TableCell>
                                            <TableCell sx={{fontWeight: 'bold', color: 'primary.main'}} align="left">{row.role}</TableCell>
                                            <TableCell sx={{fontWeight: 'bold', color: 'primary.main'}} align="right">{row.kmo}</TableCell>
                                        </TableRow>
                                    );
                                }else{
                                    return (
                                        <TableRow
                                            hover
                                            onClick={(event) => handleClick(event, row)}
                                            role="checkbox"
                                            aria-checked={isItemSelected}
                                            tabIndex={-1}
                                            key={row.id}
                                            selected={isItemSelected}
                                            sx={{ cursor: 'pointer' }}
                                        >
                                            <TableCell padding="checkbox">
                                                <Checkbox
                                                    color="primary"
                                                    checked={isItemSelected}
                                                    inputProps={{
                                                        'aria-labelledby': labelId,
                                                    }}
                                                />
                                            </TableCell>
                                            <TableCell align="left">{row.uuid}</TableCell>
                                            <TableCell align="left">{row.role}</TableCell>
                                            <TableCell align="right">{row.kmo}</TableCell>
                                        </TableRow>
                                    )
                                }
                            })}
                            {emptyRows > 0 && (
                                <TableRow
                                    style={{
                                        height: 33 * emptyRows,
                                    }}
                                >
                                <TableCell colSpan={6} />
                                </TableRow>
                            )}
                            </TableBody>
                        </Table>
                    </TableContainer>
                    <TablePagination
                        rowsPerPageOptions={[5, 10, 25]}
                        component="div"
                        count={modelList.length}
                        rowsPerPage={rowsPerPage}
                        page={page}
                        onPageChange={handleChangePage}
                        onRowsPerPageChange={handleChangeRowsPerPage}
                    />
                </Paper>
            </Box>
        </div>
    );

}