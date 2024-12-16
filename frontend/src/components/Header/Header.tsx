import React from 'react';
import styles from "./Header.module.css";

const Header: React.FC = () => {
  return (
    <header className={styles.header}>  {/* Remover as aspas ao redor de {styles.header} */}
      <h1>COMO VAI AMOR ?</h1>
    </header>
  );
};

export default Header;
