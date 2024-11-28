import { type MRT_DefinedTableOptions, type MRT_TableInstance } from '../types';
export declare const useMRT_TableInstance: <TData extends Record<string, any> = {}>(tableOptions: MRT_DefinedTableOptions<TData>) => MRT_TableInstance<TData>;
