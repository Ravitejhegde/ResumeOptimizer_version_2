import styles from "./Header.module.css";

const Header = () => {
  return (
    <header className={styles.header}>
      <div className={styles.brand}>
        <div className={styles.logo}>R</div>

        <div>
          <h1>ResumeOptimizer</h1>
          <p>Same Resume. Smarter Words.</p>
        </div>
      </div>

      <nav className={styles.actions}>
        <button>Pricing</button>
        <button>Theme</button>
        <button>Login</button>
      </nav>
    </header>
  );
};

export default Header;