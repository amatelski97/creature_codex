import { type MRT_DefinedTableOptions, type MRT_TableOptions } from '../types';
export declare const useMRT_TableOptions: <TData extends Record<string, any> = {}>(tableOptions: MRT_TableOptions<TData>) => MRT_DefinedTableOptions<TData>;
