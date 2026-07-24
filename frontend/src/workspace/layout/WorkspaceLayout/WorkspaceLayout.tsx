import type { ReactNode } from "react";
import styles from "./WorkspaceLayout.module.css";

interface Props {
  children?: ReactNode;
}

const WorkspaceLayout = ({ children }: Props) => {
  return <main className={styles.workspace}>{children}</main>;
};

export default WorkspaceLayout;