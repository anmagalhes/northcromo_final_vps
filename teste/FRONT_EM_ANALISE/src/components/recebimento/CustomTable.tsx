import React from "react";
import { ReactTabulator } from "react-tabulator";
import { CellComponent } from "tabulator-tables";  // importando tipo correto
import "react-tabulator/lib/styles.css";
import "tabulator-tables/dist/css/tabulator.min.css";

const data = [
  { id: 1, name: "João", age: 29, active: true },
  { id: 2, name: "Maria", age: 34, active: false },
  { id: 3, name: "Pedro", age: 42, active: true },
];

const columns = [
  {
    formatter: "rowSelection",
    titleFormatter: "rowSelection",
    hozAlign: "center",
    headerSort: false,
    cellClick: function (e: MouseEvent, cell: CellComponent) {
      cell.getRow().toggleSelect();
    },
    width: 50,
  },
  { title: "Nome", field: "name", editor: "input", widthGrow: 2, cssClass: "editable-cell" },
  { title: "Idade", field: "age", editor: "number", widthGrow: 1, cssClass: "editable-cell" },
  {
    title: "Ativo",
    field: "active",
    formatter: "tickCross",
    editor: true,
    widthGrow: 1,
    hozAlign: "center",
  },
];

export default function CustomTable() {
  return (
    <div className="tabulator-container" style={{ maxHeight: "1000px", overflowY: "auto" }}>
      <ReactTabulator
        data={data}
        columns={columns}
        layout={"fitColumns"}
        options={{
          selectable: true,
          movableColumns: true,
          resizableRows: true,
        }}
        className="tabulator"
      />
    </div>
  );
}
