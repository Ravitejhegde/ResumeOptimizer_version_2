import type { ReactNode } from "react";

import Header from "../Header/Header";
import WorkspaceLayout from "../WorkspaceLayout/WorkspaceLayout";

interface Props {
  children?: ReactNode;
}

const AppLayout = ({ children }: Props) => {
  return (
    <>
      <Header />
      <WorkspaceLayout>{children}</WorkspaceLayout>
    </>
  );
};

export default AppLayout;