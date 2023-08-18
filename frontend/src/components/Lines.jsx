import { Fragment } from "react";

import styles from "./Lines.module.css";

/**
 * check whether the ith line should be highlighted.
 * the current line should be highlighted
 * @param {*} index
 * @param {*} code 
 */
function colourLine(index, curr) {
  if (curr === null) return "";

  return (index === curr) ? styles.highlight : "";
}

export default function Lines({code, lines, curr}) {
  return code.map(
    (line, i) => (
      <Fragment key={`line-${i}`}>
        <span className={colourLine(i, code)}>
          {`${lines[i]}${lines[i] === "" ? "" : "."}`}
        </span>
        <span className={`${styles.preserveSpace} ${colourLine(i, curr)}`}>{line}</span>
      </Fragment>
    )
  );
} 
