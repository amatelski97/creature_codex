import { type MRT_TableInstance } from '../types';
interface Props<TData extends Record<string, any> = {}> {
    stackAlertBanner?: boolean;
    table: MRT_TableInstance<TData>;
}
export declare const MRT_ToolbarAlertBanner: <TData extends Record<string, any> = {}>({ stackAlertBanner, table, }: Props<TData>) => import("react/jsx-runtime").JSX.Element;
export {};
