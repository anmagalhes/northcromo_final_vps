import React from 'react';
import styles from "./Flooter.module.css";

const Footer: React.FC = () => {
  return (
    <footer className={styles.footer}>
        <p>
          <span className={styles.footer_span}>
            REACT
          </span>
        </p>
      </footer>
  );
};

export default Footer;